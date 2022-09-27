##Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#import spotipy
#import os
#import requests

#__name__ refers to local python file
app = Flask(__name__)
#Create secret key for website
app.config['SECRET_KEY'] = '4de316f46ad6af0ed9a5fa972606f225'

##DATABASE CONTROLS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes