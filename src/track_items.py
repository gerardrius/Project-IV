import requests
import re
import

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

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