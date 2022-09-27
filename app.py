##Imports
from flask import Flask, request, render_template, url_for, flash , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from app import routes
from forms import RegistrationForm, LoginForm
from datetime import datetime as dt
import datetime
import spotipy
import os
import requests

#__name__ refers to local python file
app = Flask(__name__)
#Create secret key for website
app.config['SECRET_KEY'] = '4de316f46ad6af0ed9a5fa972606f225'


##DATABASE CONTROLS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
#Creates user Table (class)
class User(db.Model):
    #Create tablename, may need to delete
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    track = db.relationship('Trackinsight', backref = 'author', lazy = True)
    def __repr__(self):
        return f"User('{self.email}')"
#Creates TrackInsight Class
class Trackinsight(db.Model):
    __tablename__ = "trackinsight"
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(120),db.ForeignKey('user.email'), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = dt.utcnow)
    track_content = db.Column(db.Text, nullable = False)

    #need defs

##END OF DATABASE CONTROLS


## url in website that is going to be navigated to
@app.route('/')
def home_page():
    return render_template('home.html')

#navigates to about page
@app.route('/about')
def about_page():
    '''
    Creates a page containing information about our project and it's motivations
    '''

    return render_template('about.html')

#Navigates to registration page, adds methods that allows form to get and post
@app.route('/register', methods = ['GET','POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        #checks if the form was filled out correct
        flash(f'Account created for {form.email.data}!',category = 'success')
        #redirects user to home page
        return redirect(url_for('home_page'))
    return render_template('register.html', form = form)

#Navigates to login page
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'luke.garcia2@laverne.edu' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)





if __name__ =='__main__':
    app.run(debug=True)

