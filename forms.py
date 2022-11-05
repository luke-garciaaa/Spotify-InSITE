
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
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

    #Function within form that prevents duplicate emails
    def validate_email(self,email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('An account with that email already exists.')
##END OF REGISTRATION 
class LoginForm(FlaskForm):
    
    ## create email part of registration
    email = StringField('Email', validators = [DataRequired(), Email()])

    #password registration
    password = PasswordField('Password', validators = [DataRequired(),Length(min = 2, max = 60)])
    
    submit = SubmitField('Login')
class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post')