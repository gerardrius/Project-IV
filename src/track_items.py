import requests
import re
import os
import numpy as np

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import src.credentials as cred
genius = cred.lyricsgenius.Genius(cred.geniusToken())
spotify_token  = cred.spotifyToken()
headers = cred.query_header (spotify_token)


# TRACK ITEMS (NAME, ARTIST, POPULARITY AND SONG ID)
def track_items (response):
    
    tracks = response['tracks']['items']

    dict_ = {
        'Name': [tracks[i]['track']['name'] for i in range(len(tracks))],
        'Artist': [tracks[i]['track']['artists'][0]['name'] for i in range(len(tracks))],
        'Popularity': [tracks[i]['track']['popularity'] for i in range(len(tracks))],
        'Song ID': [tracks[i]['track']['id'] for i in range(len(tracks))],
    }
    
    return dict_

# track_items_dict_ = track_items (response)

# SONG AUDIO FEATURES
def track_audio_features (dict_):
    audio_features_request_base = "https://api.spotify.com/v1/audio-features/"
    request_list = [audio_features_request_base + dict_['Song ID'][i] for i in range(len(dict_['Song ID']))]
    features = [requests.get(request, headers=headers).json() for request in request_list]

    dict_['Danceability'] = [features[i]['danceability'] for i in range(len(features))]
    dict_['Energy'] = [features[i]['energy'] for i in range(len(features))]
    dict_['Key'] = [features[i]['key'] for i in range(len(features))]
    dict_['Loudness'] = [features[i]['loudness'] for i in range(len(features))]
    dict_['Mode'] = [features[i]['mode'] for i in range(len(features))]
    dict_['Speechiness'] = [features[i]['speechiness'] for i in range(len(features))]
    dict_['Acousticness'] = [features[i]['acousticness'] for i in range(len(features))]
    dict_['Instrumentalness'] = [features[i]['instrumentalness'] for i in range(len(features))]
    dict_['Liveness'] = [features[i]['liveness'] for i in range(len(features))]
    dict_['Valence'] = [features[i]['valence'] for i in range(len(features))]
    dict_['Tempo'] = [features[i]['tempo'] for i in range(len(features))]
    return dict_

# track_items_dict_ = track_audio_features ()


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
def get_lyrics(dict_):
    lyrics_list = []
    for i in range(len(dict_['Name'])):
        song = genius.search_song(dict_['Name'][i], dict_['Artist'][i])
        if song is not None:
            try:
                lyrics_list.append(clean_lyrics(song.lyrics))
            except:
                lyrics_list.append(np.nan)
        else:
            lyrics_list.append(np.nan)
    
    dict_['Lyrics'] = lyrics_list
    return dict_


# SONG LYRICS SENTIMENT ANALYSIS
sia = SentimentIntensityAnalyzer()

def track_sentiment (dict_):
    positive = []
    negative = []
    neutral = []
    compound = []

    for i in range(len(dict_['Lyrics'])):
        try:
            sentiment_analysis = sia.polarity_scores(dict_['Lyrics'][i])
            positive.append(sentiment_analysis['pos'])
            neutral.append(sentiment_analysis['neu'])
            negative.append(sentiment_analysis['neg'])
            compound.append(sentiment_analysis['compound'])
        except:
            positive.append(np.nan)
            neutral.append(np.nan)
            negative.append(np.nan)
            compound.append(np.nan)

    dict_['Positive'] = positive
    dict_['Neutral'] = neutral
    dict_['Negative'] = negative
    dict_['Compound'] = compound

    return dict_