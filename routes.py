from flask import request, render_template, url_for, flash , redirect, Flask
from app import app, db, bcrypt
from app.models import User, Trackinsight
from app.forms import RegistrationForm, LoginForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import request, session, redirect,url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time

TOKEN_INFO = 'token_info'
###  BEGINNING OF SPOTIFY ###

##basically the redirect
@app.route('/instantspot')
def instantspot():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
   
    

@app.route('/authorize')
def authorize_page(): 
    flash(f'Your Spotify Account has been authorized!',category = 'success')
    sp_oauth = create_spotify_oauth()
    #session.clear()                   #########################################################################
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info

    #takes user to track_page after authorization
    return redirect(url_for('track_testing'))
    


def create_spotify_oauth():
    return SpotifyOAuth(
        #client_id = os.environ.get("SPOTIPY_CLIENT_ID"),
        #client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET"),
        client_id = 'ba112b111926424ebe76312e1c82187e',
        client_secret = 'c603209cb1cb4cb49bfcac2fd557e159',
        ### YES YES IT WORK OMG 
        redirect_uri = 'http://localhost:5000/authorize',
        ## URL_FOR SUCKS AND DOESNT WORK
        scope = "user-top-read"
        #scope = "user-library-read"
        
    )

@app.route('/tracktest', methods = ['GET', 'POST'])
def track_testing():
    
    try:
        token_info = get_token()
    except:
        print('User not logged in')
        redirect(url_for('authenticate_page'))
    sp = spotipy.Spotify(auth = token_info['access_token'])
    ######### BEGINNING OF INSIGHT IMPLEMENTATION
    ranges = ['short_term', 'medium_term', 'long_term']
    artist_info = []
    for sp_range in ['short_term', 'medium_term', 'long_term']:
        results = sp.current_user_top_artists(time_range=sp_range, limit=50)
        for i, item in enumerate(results['items']):
            artist_info.append(item['name'])
    artist_name = artist_info[0]
    
    post = Trackinsight(track_content = artist_name, user_email = current_user.email) ##works except for current_user.email
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('track_page'))         
    

    ## ENDING OF INSIGHT IMPLEMENTATION
   #### PUT SONG INFO HERE 
    #song_info = sp.current_user_top_artists(time_range='short_term', limit=50)
    #return song_info
    #return sp.current_user_saved_tracks(limit = 50, offset = 0)



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info
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
            session.permanent = False    ################### IF THE BROWSER RESTARTS, SO DOES THE SESSION
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
#@app.route('/tpost/new', methods = ['GET', 'POST'] )
#@login_required
#def tpost_page():
#    form = PostForm()
#    if form.validate_on_submit():
#        post = Trackinsight(track_content = form.content.data, user_email = current_user.email)
#        db.session.add(post)
#        db.session.commit()
#        flash('Your post has been created!', 'success')
#        return redirect(url_for('home_page'))
#    return render_template('tpost.html', title = 'New Post', form = form)


