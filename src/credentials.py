import os
import requests
import pandas as pd
from dotenv import load_dotenv

import lyricsgenius
from getpass import getpass
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import numpy as np

# Insert Genius token (in case it expires: https://genius.com/api-clients)
genius_token = getpass()
genius = lyricsgenius.Genius(genius_token)

# Example Playlist link:
playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=b705194596334305'

def spotifyToken ():
    """This function refreshes a token for a given app on Spotify
    returns: token as a string
    """

    # 1. Defining: credentials fot the app
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

token  = spotifyToken()

def query_header (token):
    return {"Authorization":f"Bearer {token}"}

headers = query_header (token)

# PLAYLIST RESPONSE
def playlist_id ():
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

def track_items ():
    
    tracks = response['tracks']['items']

    track_items_dict = {
        'Name': [tracks[i]['track']['name'] for i in range(len(tracks))],
        'Artist': [tracks[i]['track']['artists'][0]['name'] for i in range(len(tracks))],
        'Popularity': [tracks[i]['track']['popularity'] for i in range(len(tracks))],
        'Song ID': [tracks[i]['track']['id'] for i in range(len(tracks))],
    }
    
    return track_items_dict

track_items_dict = track_items ()

def track_audio_features ():
    audio_features_request_base = "https://api.spotify.com/v1/audio-features/"
    request_list = [audio_features_request_base + track_items_dict['Song ID'][i] for i in range(len(track_items_dict['Song ID']))]
    features = [requests.get(request, headers=headers).json() for request in request_list]

    track_items_dict['Danceability'] = [features[i]['danceability'] for i in range(len(features))]
    track_items_dict['Energy'] = [features[i]['energy'] for i in range(len(features))]
    track_items_dict['Key'] = [features[i]['key'] for i in range(len(features))]
    track_items_dict['Loudness'] = [features[i]['loudness'] for i in range(len(features))]
    track_items_dict['Mode'] = [features[i]['mode'] for i in range(len(features))]
    track_items_dict['Speechiness'] = [features[i]['speechiness'] for i in range(len(features))]
    track_items_dict['Acousticness'] = [features[i]['acousticness'] for i in range(len(features))]
    track_items_dict['Instrumentalness'] = [features[i]['instrumentalness'] for i in range(len(features))]
    track_items_dict['Liveness'] = [features[i]['liveness'] for i in range(len(features))]
    track_items_dict['Valence'] = [features[i]['valence'] for i in range(len(features))]
    track_items_dict['Tempo'] = [features[i]['tempo'] for i in range(len(features))]
    return track_items_dict

track_items_dict = track_audio_features ()

def get_lyrics():
    lyrics_list = []
    for i in range(len(track_items_dict['Name'])):
        song = genius.search_song(track_items_dict['Name'][i], track_items_dict['Artist'][i])
        if song is not None:
            try:
                lyrics_list.append(song.lyrics)
            except:
                lyrics_list.append(np.nan)
        else:
            lyrics_list.append(np.nan)
    
    track_items_dict['Lyrics'] = lyrics_list
    return track_items_dict
    


def track_sentiment ():
    pass

