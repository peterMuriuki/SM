from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, length, Regexp, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    """
    Defines the registration form: fields:
    user_name: string that uses regular expressions to accept the default required characters for u-names
    password: length: > 8 characters
    password confirmation:  same as password
    email: valid email, # confirmation message sent to email
    """
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    name = StringField('Name', validators=[InputRequired(), DataRequired(), length(5, 64),
                                        Regexp('^[A-Za-z][A-Za-z0-9_ ]*$', 0, 'Name can only contain numbers, space or underscores')])
    user_name = StringField('user name', validators=[DataRequired(), InputRequired(), length(min=3, max=50), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
                                                                    0, 'Name can only contain letters, numbers, or underscores')])
    password = PasswordField('password', validators=[DataRequired(), InputRequired(), length(min=8, max=100), EqualTo('repassword', message='Passwords should match')])
    repassword = PasswordField('confirm Password', validators=[DataRequired(), length(min=8, max=100), InputRequired()])
    submit = SubmitField('sign up')



class LoginForm(FlaskForm):
    """defines the cloass template for creating login forms: fields:
    user_name and password
    """
    user_name = StringField(' user name', validators=[DataRequired(), InputRequired(), length(min=5, max=50), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
                                                                    0, 'Name can only contain letters, numbers, or underscores')])
    password = PasswordField('password', validators=[DataRequired(), InputRequired()])
    rem = BooleanField('Keep me logged in')
    submit = SubmitField(' log in')

class GeneralProfile(FlaskForm):
    """Templating the profile page's form for user data modification"""
    name = StringField('Name: ', validators=[ length(5, 64),
                                        Regexp('^[A-Za-z][A-Za-z0-9_ ]*$', 0, 'Name can only contain numbers, space or underscores')])
    user_name = StringField('user name: ', validators=[length(min=3, max=50), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
                                                                    0, 'Name can only contain letters, numbers, or underscores')])
    submit = SubmitField('SAVED')
    
class EmailProfile(FlaskForm):
    """Template for changing and modifying the email"""
    email = StringField('New Email: ', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password Authentication: ', validators=[DataRequired(), length(min=8, max=100), InputRequired()])
    submit = SubmitField('SAVE')
    
    
class PasswordProfile(FlaskForm):
    """Template for changing and modfying the password"""
    old_password = PasswordField('current password: ', validators=[DataRequired(), InputRequired(),length(min=8, max=100)])
    new_password = PasswordField('new password: ', validators=[DataRequired(), InputRequired(), length(min=8, max=100), EqualTo('repassword', message='Passwords should match')])
    repassword = PasswordField('confirm new Password: ', validators=[DataRequired(), length(min=8, max=100), InputRequired()])
    submit = SubmitField('SAVE')
    
class SecondaryProfile(FlaskForm):
    """Dont even ask"""
    plan = SelectField('plan: ', choices=[('dob','double or nothing')])
    submit = SubmitField('SAVE')