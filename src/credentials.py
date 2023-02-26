import pandas as pd
import numpy as np

# To reach .env Spotify and Genius API credentials
import os
import requests
from dotenv import load_dotenv

# For lyrics
import lyricsgenius
from getpass import getpass

import re
import string

# For sentiment analysis
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# For linking the resulting Dataframe with MySQL workbench
import mysql.connector as msql
from mysql.connector import Error
import pymysql
import sqlalchemy as alch

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

# TRACK ITEMS (NAME, ARTIST, POPULARITY AND SONG ID)
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

# SONG AUDIO FEATURES
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


# CLEAN LYRICS
def clean_lyrics(lyrics):
    # Remove text in square brackets
    lyrics = re.sub(r'\[.*?\]', '', lyrics)
    
    # Remove text in parentheses
    lyrics = re.sub(r'\(.*?\)', '', lyrics)
    
    # Remove blank lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    
    # Remove leading/trailing whitespace characters
    lyrics = lyrics.strip()
    
    return lyrics

# SONG LYRICS
def get_lyrics():
    lyrics_list = []
    for i in range(len(track_items_dict['Name'])):
        song = genius.search_song(track_items_dict['Name'][i], track_items_dict['Artist'][i])
        if song is not None:
            try:
                lyrics_list.append(clean_lyrics(song.lyrics))
            except:
                lyrics_list.append(np.nan)
        else:
            lyrics_list.append(np.nan)
    
    track_items_dict['Lyrics'] = lyrics_list
    return track_items_dict


# SONG LYRICS SENTIMENT ANALYSIS
sia = SentimentIntensityAnalyzer()

def track_sentiment ():
    positive = []
    negative = []
    neutral = []
    compound = []

    for i in range(len(track_items_dict['Lyrics'])):
        try:
            sentiment_analysis = sia.polarity_scores(track_items_dict['Lyrics'][i])
            positive.append(sentiment_analysis['pos'])
            neutral.append(sentiment_analysis['neu'])
            negative.append(sentiment_analysis['neg'])
            compound.append(sentiment_analysis['compound'])
        except:
            positive.append(np.nan)
            neutral.append(np.nan)
            negative.append(np.nan)
            compound.append(np.nan)

    track_items_dict['Positive'] = positive
    track_items_dict['Neutral'] = neutral
    track_items_dict['Negative'] = negative
    track_items_dict['Compound'] = compound

    return track_items_dict

# SONG TOPIC RECOGNITION



# SAVE DATAFRAME AS CSV TO IMPORT IT TO MYSQL WORKBENCH:
df = pd.DataFrame(track_items_dict)

def dataframe_to_sql ():
    passwd = os.getenv('sql_pw')
    dbName = 'spotify'

    try:
        conn = msql.connect(host='localhost', user='root', password=passwd)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
            print("Database is created")
    except Error as e:
        print("Error while connecting to MySQL", e)

    connectionData=f"mysql+pymysql://root:{passwd}@localhost/{dbName}"
    engine = alch.create_engine(connectionData)

    df.to_sql(name='playlist_items', con=engine, if_exists='replace', index=False)