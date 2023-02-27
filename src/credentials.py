import pandas as pd
import numpy as np

# To reach .env Spotify and Genius API credentials
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# For lyrics
import lyricsgenius

# Example Playlist link:
playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=b705194596334305'

# Genius Token
def geniusToken():
    client_id = os.getenv('genius_id')
    client_secret = os.getenv('genius_key')

    url = 'https://api.genius.com/oauth/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    if response.ok:
        genius_token = response.json()['access_token']
        return genius_token
    else:
        raise ValueError('Failed to get access token from Genius API')

genius = lyricsgenius.Genius(geniusToken())

# Spotify Token
def spotifyToken ():
    """This function refreshes a token for a given app on Spotify
    returns: token as a string
    """

    # 1. Defining: credentials for the app
    client_id = os.getenv("id")
    client_secret = os.getenv("secret")
    
    #2. Request
    body_params = {"grant_type":"client_credentials"}
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data=body_params, auth=(client_id,client_secret))
    
    try:
        token = response.json()["access_token"]
        return token

    except:
        print("The request did not go through: wrong credentials!")

# SPOTIFY TOKEN AND QUERY HEADER:
spotify_token  = spotifyToken()

def query_header (spotify_token = spotify_token):
    return {"Authorization":f"Bearer {spotify_token}"}

headers = query_header (spotify_token)