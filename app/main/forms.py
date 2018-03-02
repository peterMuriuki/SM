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
    
    
class GeneralProfile(FlaskForm):
    """Templating the profile page's form for user data modification"""
    name = StringField('Name: ', validators=[ length(5, 64),
                                        Regexp('^[A-Za-z][A-Za-z0-9_ ]*$', 0, 'Name can only contain numbers, space or underscores')])
    user_name = StringField('user name: ', validators=[length(min=3, max=50), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
                                                                    0, 'Name can only contain letters, numbers, or underscores')])
    
class EmailProfile(FlaskForm):
    """Template for changing and modifying the email"""
    email = StringField('New Email: ', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password Authentication: ', validators=[DataRequired(), length(min=8, max=100), InputRequired()])
    submit = SubmitField('SAVE')
    
    
class PasswordProfile(flaskForm):
    """Template for changing and modfying the password"""
    old_password = PasswordField('current password: ', validators=[DataRequired(), InputRequired(),length(min=8, max=100)])
    new_password = PasswordField('new password: ', validators=[DataRequired(), InputRequired(), length(min=8, max=100), EqualTo('repassword', message='Passwords should match')])
    repassword = PasswordField('confirm new Password: ', validators=[DataRequired(), length(min=8, max=100), InputRequired()])
    submit = SubmitField('SAVE')
    
class SecondaryProfile(FlaskForm):
    """Dont even ask"""
    plan = SelectField('plan: ', choices=[('dob','double or nothing')])
    submit = SubmitField('SAVE')