from flask import request, render_template, url_for, flash , redirect
from app import app
from app.models import User, Trackinsight
from app.forms import RegistrationForm, LoginForm


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