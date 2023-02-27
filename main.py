import pandas as pd
import src.creds as cred
import src.response as resp
import src.track_items as track
import src.genre_classifier as genre
import src.sql_connection as sql

# please, input a playlist link:
playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=b705194596334305'

# Credentials
genius = cred.lyricsgenius.Genius(cred.geniusToken())
spotify_token  = cred.spotifyToken()
headers = cred.query_header (spotify_token)

# Responses
query = resp.playlist_query ()
response = resp.playlist_response()

# Track items
result_dict = track.track_items (response)
result_dict = track.track_audio_features (result_dict)
result_dict = track.get_lyrics(result_dict)                            
result_dict = track.track_sentiment(result_dict)

spotify_dataframe = pd.DataFrame(result_dict)

# Genre classifier
data_to_train_model = genre.model_data ('data/spotify_genre_final.xlsx')
my_rfc = genre.get_rfc(data_to_train_model)
my_genre_predictions = genre.genre_predictor(spotify_dataframe, my_rfc)
result_df = genre.df_append_genre(spotify_dataframe, my_genre_predictions)

# SQL connection and export DataFrame as table
sql.dataframe_to_sql (result_df, 'todays_top_hits')