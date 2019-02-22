from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Required, Email, DataRequired, ValidationError, Optional
from flask import g

class StartForm(FlaskForm):
    
    submit = SubmitField('Start')

class SignupForm(FlaskForm):
    name = TextField('<h4><b> Please enter a unique key (e.g. name_id) to identify the data you are labelling. This is necessary so that you can manage multiple sets of data you may be labelling, and allows you to continue labelling even though your session has ended. </b></h4>', validators=[Required()])

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