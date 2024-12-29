from flask import Flask, render_template, request, session, redirect, url_for
import os
from dotenv import load_dotenv
from flask_session import Session
import urllib.parse
import base64
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# important variables
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/me/top/'
scope = 'user-top-read'


# Configuring session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)



# Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')



# Login page (creates authorization url and redirects to it)
@app.route("/login", methods=["GET"])
def login():
    
    # creating query of params from spotify documentation
    query_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    # parses query_params using urllib.parse
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(query_params)}"

    # redirects to the auth_url
    return redirect(auth_url)



# Callback page (sends HTTP POST request and receives token_info, storing in session)
@app.route("/callback", methods=["GET", "POST"])
def callback():

    # getting code from redirect uri
    auth_code = request.args.get('code')

    # creating the HTTP header (from Spotify documentation)
    # first encoding credentials in base64 format
    base64_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    auth_header = {
        'Authorization': 'Basic ' + base64_credentials,
        'content-type': 'application/x-www-form-urlencoded'
    }


    # creating body parameters (from Spotify documentation)
    body_param = {
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    # making the POST request
    response = requests.post(TOKEN_URL, headers=auth_header, data=body_param)

    # extracting access and refresh tokens
    token_info = response.json()
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    expires_in = token_info['expires_in']

    # storing token info in session
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['expires_at'] = datetime.now().timestamp() + expires_in


    # redirecting to customization page
    return redirect(url_for("customize"))



# Customization page
@app.route("/customize", methods=["GET"])
def customize():
    return render_template('customize.html')

@app.route("/refresh", methods=["GET"])
def refresh():
    refresh_token = session['refresh_token']

    # checking if refresh_token present
    if not refresh_token:
        return redirect(url_for('login'))
    
    if datetime.now().timestamp() > session['expires_at']:
        query_body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

    token_info = requests.post(TOKEN_URL, data=query_body)
    token_info = token_info.json()

    expires_in = token_info['expires_in']
    session['access_token'] = token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + expires_in

    return redirect(url_for("customize"))


# Top Artists page
@app.route("/topData", methods=["GET"])
def topData():

    # Getting access token
    access_token = session['access_token']

    # checking if access_token present
    if not access_token:
        return redirect(url_for('login'))
    # checking if access_token needs refresh
    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for("refresh"))

    # putting the header together
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    # getting user variables
    type = request.args.get('type')
    time_period = request.args.get('time_period')
    length = int(request.args.get('length'))

    print(f"Type: {type}, Time Period: {time_period}, Length: {length}")

    
    url = f"{API_BASE_URL}{type}?time_range={time_period}&limit={length}&offset=0"

    top_data_response = requests.get(url, headers=headers)

    # Check for HTTP errors
    if top_data_response.status_code != 200:
        print(f"API Error: {top_data_response.status_code}, {top_data_response.text}")
        return f"Error fetching data: {top_data_response.status_code}"
    

    top_data = top_data_response.json()

    top_items = top_data["items"]

    return render_template('topData.html', type=type, time_period=time_period, top_data=top_data, top_items=top_items)


# handling logging out
@app.route("/logout", methods=["GET"])
def logout():

    session.pop("token_info", None)
    return redirect(url_for("index"))


# Runner
if __name__ == '__main__':
    app.run(debug=True)