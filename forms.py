
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
#REGISTRATION##
class RegistrationForm(FlaskForm):
    #username = StringField('Username', 
    #validators = [DataRequired(), Length(min = 2, max = 20)])

    ## create email part of registration
    email = StringField('Email', validators = [DataRequired(),Email()])

    #password registration
    password = PasswordField('Password', validators = [DataRequired(),Length(min = 2, max = 60)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')
##END OF REGISTRATION 
class LoginForm(FlaskForm):
    
    ## create email part of registration
    email = StringField('Email', validators = [DataRequired(), Email()])

    #password registration
    password = PasswordField('Password', validators = [DataRequired(),Length(min = 2, max = 60)])
    
    submit = SubmitField('Login')
