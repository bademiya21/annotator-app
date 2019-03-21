# This file contains the app frontend
from application import db

from functools import lru_cache
from flask import request, session, current_app, Blueprint, render_template, redirect, url_for, g, send_from_directory
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_wtf import FlaskForm
from wtforms.fields import *
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from application.forms import *
from application.nav import nav
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
from application.email import send_password_reset_email
import os
import pandas as pd

frontend = Blueprint('frontend', __name__)

# This code adds a navbar
@nav.navigation()
def navbar():

    if current_user.is_authenticated:
        return Navbar(
            View("Home", ".index"),
            View('Upload Data', '.upload_data'),
            View("Logout {}".format(current_user.username), ".logout")
        )
    else:
        return Navbar(
            View("Home", ".index"),
            View("Login", ".login")
        )

nav.register_element('frontend_top', navbar)

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.upload_data'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@frontend.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            send_password_reset_email(user)
        return redirect(url_for('.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@frontend.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('reset_password.html', form=form)


@frontend.route('/logout')
def logout():
    #session.pop(current_user.username)
    logout_user()
    return redirect(url_for('.index'))


@frontend.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)


@frontend.route('/')
@frontend.route('/index')
def index():

    # Create form that starts process
    start_form = StartForm()

    #if start_form.validate_on_submit():
    #return redirect(url_for('.login'))

    return render_template('index.html', form=start_form)


@frontend.route('/end/')
@login_required
def end():
    try:
        return render_template('end.html', res_filename=request.args['att_name'], orig_filename=request.args['orig_name'])
    except Exception as e:
        return str(e)

# Create upload form which allows users to upload data
@frontend.route('/upload-data/', methods=('GET', 'POST'))
@login_required
def upload_data():
    form = UploadForm()

    if form.validate_on_submit():

        f = form.sample_file.data
        filename = os.path.splitext(secure_filename(f.filename))[0] + "_" + current_user.username + os.path.splitext(secure_filename(f.filename))[1]

        # Save file into disk for it to be read later - this is better than
        # reading it into memory especially for large files, note that a data
        # folder must be created
        data_dir = os.path.join(current_app.root_path, 'uploaded-data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        f.save(os.path.join(data_dir, filename))

        # Redirect to page to that shows samples of data
        return redirect(url_for('.display_data', f_name=filename))

    return render_template('upload.html', form=form)

# Create template to display csv using pandas and provide fields to input labels


@frontend.route('/display-data', methods=('GET', 'POST'))
@login_required
def display_data():

    # Filenames are passed as HTTP requests
    filename = request.args['f_name']
    file_path = os.path.join(current_app.root_path, 'uploaded-data', filename)

    # Use lru_cache function to prevent multiple file I/O
    df = read_df(file_path)

    # Set number of characters to show in sample data
    pd.set_option('display.max_colwidth', 1000)

    cols = list(df)

    # Pass list of column names to DisplayForm, which will then be selected for
    # labelling
    form = DisplayForm(vals=cols)

    total_length = len(df)
    disp_len = 0

    if form.validate_on_submit():
        if (form.annotate.data):  # Check if SubmitField is clicked for 'sample' or 'annotate'
            #session.clear()
            # This counter is needed to reference the pandas dataframe index
            session[current_user.username] = 0
            #session['counter'] = 0

            # Pass filename, colnames, and labels to annotate data view
            return redirect(url_for('.annotate_data', f_name=filename, colname=form.sel_col.data, labels=form.labels.data))
        # Parameter for number of rows of samlpe data to show
        disp_len = int(form.num_rows.data)

    return render_template('display.html', f_name=filename, length=total_length, dataframe=df.sample(n=disp_len).to_html(), form=form, cols=cols)

# Route for annotating data, which is a separate page that will show the text
# and buttons to label the text


@frontend.route('/annotate_data/', methods=('GET', 'POST'))
@login_required
def annotate_data():

    filename = request.args['f_name']
    filename_sav = filename.split(".")[0]
    colname = request.args['colname']
    col_label = colname + '_label'
    labels = request.args['labels'].split(';')

    # Note that a 'data' folder must be created
    file_path = os.path.join(current_app.root_path, 'uploaded-data', filename)
    res_filename = filename_sav + '_' + col_label + '.csv'
    res_file = os.path.join(current_app.root_path, 'data', res_filename)
    df = read_df(file_path)

    # Read last line and increase counter if lines are already labelled and
    # continue from there, so users can continue labelling even if they close
    # their computer Cannot use cached function for reading DF because file is
    # constantly updated
    if (session[current_user.username] == 0) and os.path.isfile(res_file):
        res_df = read_df(res_file)
        session[current_user.username] = res_df.index[-1] + 1

    # Create class AnnotateForm and dynamically add label buttons
    class AnnotateForm(FlaskForm):
        pass

    for lab in labels:
        setattr(AnnotateForm, lab, SubmitField())

    form = AnnotateForm()

    add_label_form = AddLabelForm()

    label_clicked = False
    for key, value in form.data.items():
            if value is True:
                label_clicked = True

    # This is executed if the user clicks on one of the label buttons
    if form.validate_on_submit() and label_clicked:

        row = df.iloc[[session[current_user.username]]]
        for key, value in form.data.items():
            if value is True:
                # Label row with button clicked
                row[col_label] = key

        if not os.path.exists(os.path.dirname(res_file)):
            os.makedirs(os.path.dirname(res_file))

        with open(res_file, 'a', encoding="utf-8", newline='') as f:
            if session[current_user.username] == 0:
                print_header = True
            else:
                print_header = False

            row.to_csv(f, header=print_header, index=False, encoding='utf-8')

        session[current_user.username] += 1
        if session[current_user.username] > len(df.index)-1:
            return redirect(url_for('.end', att_name=res_filename, orig_name=filename))

    if add_label_form.validate_on_submit() and add_label_form.add_lab.data:
        labels.extend(add_label_form.new_lab.data.split(';'))
        # Pass filename, colnames, and labels to annotate data view
        return redirect(url_for('.annotate_data', f_name=filename, colname=colname, labels=";".join(labels)))

    if session[current_user.username] > len(df.index)-1:
        return redirect(url_for('.end', att_name=res_filename, orig_name=filename))
    else:
        # Show text for labelling within jumbotron
        text = df.at[session[current_user.username], colname]

    return render_template('annotate.html', form=form, add_label_form=add_label_form, text_string=text, length=session[current_user.username]+1, total_length=df.shape[0], res_filename=res_filename, orig_filename=filename)


@frontend.route('/return_file', methods=['GET', 'POST'])
@login_required
def return_files_tut():
    filename = request.args.get('filename', None)
    try:
        saved_path = os.path.join(current_app.root_path, 'data')
        response = send_from_directory(
            directory=saved_path, filename=filename, as_attachment=True)
        response.cache_control.max_age = 0  # e.g. 1 minute
        return response
    except Exception as e:
        return str(e)


@frontend.route('/delete_files', methods=['GET', 'POST'])
@login_required
def delete_files():
    orig_filename = request.args.get('orig_filename', None)
    filename = request.args.get('filename', None)
    try:
        saved_path_orig = os.path.join(
            current_app.root_path, 'uploaded-data', orig_filename)
        os.remove(saved_path_orig)
        saved_path = os.path.join(current_app.root_path, 'data', filename)
        os.remove(saved_path)

        class DeleteForm(FlaskForm):
            pass

        form = DeleteForm()
        return render_template('delete.html', form=form)
    except Exception as e:
        return str(e)

# Use lru cache to minimise multiple file I/O
@lru_cache(maxsize=32)
@login_required
def read_df(filepath):
    if filepath.lower().endswith('.csv'):
        return pd.read_csv(filepath, encoding='utf-8')
    elif filepath.lower().endswith('.xlsx') or filepath.lower().endswith('.xls'):
        return pd.read_excel(filepath)
    else:
        raise ValueError(
            'Wrong file format! Please use CSV or Excel (xlsx or xls) format files')
