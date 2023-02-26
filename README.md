# Project-IV
Fourth Project of the Data Analysis Bootcamp


Data sources:
Spotify Developer API: to get any playlist
Spotipy Audio Features (by song URI): for audio features analysis, e.g. danceability, energy, tempo, etc
Genius getLyrics API: for sentiment analysis (positiveness, negativeness, neutrality and compound)
: sentiment analysis to human emotion


Objective of Data Obtention:
### Create a Dataframe storing Playlist relevant information
- Name
- Artist
- Album
- URI
- Audio features
    - Danceability
    - Energy
    - loudness
    - Spechiness
    - Valence
    - Liveness
    - Tempo
    - etc.
- Lyrics
- Sentiment Analysis
- Main topic of the song (love, )***


### Pandas Dataframe to CSV -> import data in MySQL Workbench
- Set a connection with MySQL Workbench
- Create a new database
- Export the Dataframe into a new table in the dataset


### Visualizations


1. Define song emotions
- Create visualizations on that

1.1. Suggest according to emotion:
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recommendations

2. Compare two different playlist and run some Hypotheses testing on similarity (e.g. on Top Hits per Country), and judge common points on different countries' musical tastes.

