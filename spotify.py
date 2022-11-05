##
###
#transferred all code to routes.py ik that's cringe

##
#from flask import request, session, redirect,url_for
#import spotipy
#from spotipy.oauth2 import SpotifyOAuth
#import os



#def redirect():
#    return 'redirect'
#def create_spotify_oauth():
#    return SpotifyOAuth(
#        client_id = os.environ.get("SPOTIPY_CLIENT_ID"),
#        client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET"),
#        #may have an issue with redirect
#        spotify_redirect_uri = url_for('home_page', external = True),
#        scope = "user-top-read" + "user-library-read"
#    )