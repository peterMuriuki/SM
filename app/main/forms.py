""""""
from wtforms import StringField, PasswordField, SubmitField, TextAreaField,  DateField
from wtforms.validators import DataRequired, InputRequired, Email, length, EqualTo, Regexp
from flask_wtf import FlaskForm

class ConfirmationForm(FlaskForm):
    """
    :template for creating the confirmation details for stake and administrators predictions analysis
    """
    confirmation_text = TextAreaField('', validators=[InputRequired(), DataRequired(), length(min=0)])
    submit = SubmitField('confirm')

class FilterForm(FlaskForm):
    """Templates the filter functions; these are to be used to request predictions more specifically"""
    first_date = DateField('from:', validators=[InputRequired(), DataRequired()])
    second_date = DateField('to:', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('filter')

class AdminFilterForm(FlaskForm):
    """Templates the filter functions; these are to be used to request predictions more specifically"""
    date = DateField('date:', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('filter')
    
   
