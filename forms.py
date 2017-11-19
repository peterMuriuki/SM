""""""
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, length, EqualTo, Regexp
from flask_wtf import FlaskForm


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
    user_name = StringField('user name', validators=[DataRequired(), InputRequired(), length(min=5, max=50), Regexp('^[A-Za-z][A-Za-z0-9_]*$',
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
    submit = SubmitField(' log in')