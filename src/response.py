# PLAYLIST RESPONSE
import requests
from src.credentials import *

def playlist_id (playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=b705194596334305'):
    """
    Function that provides the id of a playlist to put it together with the base URL.
    """
    return playlist_link.split("/")[-1].split("?")[0]

def playlist_query ():
    """
    Function that returns the actual query to be passed into the Spotify API request.
    Accepts the whole playlist url, takes the id and adds it to base URL to
    return the actual query.
    """
    url_base = "https://api.spotify.com/v1/playlists/"
    return url_base + playlist_id()

query = playlist_query ()

def playlist_response ():
    """
    Provides the response from Spotify API in json format
    Takes the query to be passed to the API
    and returns a response with the playlist items.
    """
    response = requests.get(query, headers=headers).json()
    return response

response = playlist_response()