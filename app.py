from flask import Flask, render_template, request, session, redirect, url_for
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

app = Flask(__name__)


# important variables
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')


# initializing Spotipy object
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='user-top-read',
        open_browser=False
    )
)


# Home Page
@app.route("/", methods=["GET"])
def index():
    print("redirect URL: ", SPOTIPY_REDIRECT_URI)
    return render_template('index.html')



# Login page
@app.route("/login", methods=["GET"])
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


# Callback page, deals with access and authorization codes
@app.route("/callback", methods=["GET"])
def callback():

    # get authorization code
    auth_code = request.args.get("code")
    if not auth_code:
        return "Authorization failed. No code provided", 400
    
    # get access token with authorization code
    access_token = sp.auth_manager.get_access_token(code = auth_code, as_dict=True)
    
    # storing access token in session so user won't have to sign in again
    session['access_token'] = access_token['access_token']
    
    # redirecting to customization page
    return redirect(url_for("customize"))


# Customization page
@app.route("/customize", methods=["GET"])
def customize():
    return render_template('customize.html')







# Runner
if __name__ == '__main__':
    app.run(debug=True)