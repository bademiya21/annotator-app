from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Required, Email, DataRequired, ValidationError, Optional, EqualTo
from flask import g
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from application.models import User

class StartForm(FlaskForm):
        
    pass

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UploadForm(FlaskForm):
    
    # Custom validator to check that file is csv
    def validate_file(form, field):
        
        if not (field.data.filename.endswith('csv') or field.data.filename.endswith('xls') or field.data.filename.endswith('xlsx')):
            raise ValidationError('Not a CSV or Excel file!')

    sample_file = FileField(u'<h4><b>Your .csv, .xls or .xlsx file </b></h4>', validators=[Required(), validate_file])
    
    
    submit = SubmitField(u'Upload')
    

class DisplayForm(FlaskForm):

    def __init__(self, vals = None, **kw):
        super(DisplayForm, self).__init__(**kw)
        
        # Create list of tuples because SelectField choices requires it
        tup_list = []
        for val in vals:
            tup_list.append((val, val))
        self.sel_col.choices = tup_list
    
    num_rows = SelectField(u'Sample a Number of Rows', choices = [(str(i), str(i)) for i in range(5,50,5)], validators = [Required()])
    
    sample = SubmitField(u'Sample', validators=[Optional()])

    sel_col = SelectField(u'Select column to annotate')
    labels = TextField(u'Type in label/category/class names separated by a \';\'')
      
    annotate = SubmitField(u'Annotate', validators=[Optional()])  

class AddLabelForm(FlaskForm):

    new_lab = TextField('Type any additional label names, one at a time.', default = "")

    add_lab = SubmitField('Add Labels')    

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')