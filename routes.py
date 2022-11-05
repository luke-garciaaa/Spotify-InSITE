from flask import request, render_template, url_for, flash , redirect
from app import app, db, bcrypt
from app.models import User, Trackinsight
from app.forms import RegistrationForm, LoginForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import request, session, redirect,url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


###  BEGINNING OF SPOTIFY ###


### END OF SPOTFY ###
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
    ## REMEMBER TO CHANGE
    return render_template('about.html')

#Navigates to registration page, adds methods that allows form to get and post
@app.route('/register', methods = ['GET','POST'])

def register_page():
    #checks if current user is authenticated, redirects to home page
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    #initializes class
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashes password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password= hashed_password)
        #Add user to database
        db.session.add(user)
        db.session.commit()
        #checks if the form was filled out correct
        flash(f'Your account has been created!',category = 'success')


        #redirects user to home page
        return redirect(url_for('login_page'))
    return render_template('register.html', form = form)

#Navigates to login page
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    #checks if current user is authenticated, redirects to home page
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        # checks if user exists, if user doesn't exist, will return none,
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are now logged in!', category = 'success')
            return redirect(url_for('home_page'))
            
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)
##BEGINNING OF LOGIN ONLY PAGES

#Navigates to Authenticate Spotify page, will likely need to add 
@app.route('/authenticate')
@login_required
def authenticate_page():
    
    return render_template('authenticate.html')

#page to manage tracks
@app.route('/tracks')
@login_required
def track_page():
    return render_template('tracks.html')
    
#logout page route, directs user back to home page when user is logged out             
@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))

##page to create posts, pseudo - manage tracks
@app.route('/tpost/new', methods = ['GET', 'POST'] )
@login_required
def tpost_page():
    form = PostForm()
    if form.validate_on_submit():
        post = Trackinsight(track_content = form.content.data, user_email = current_user.email)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template('tpost.html', title = 'New Post', form = form)


