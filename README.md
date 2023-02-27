### **Project-IV: Extraction | SQL | NLTK | Tableau**

---

# SPOTIFY PLAYLIST ANALYSIS


## Introduction

This project aims to provide an analysis of the set of tracks that conform any given Spotify Playlist. It covers the musical dimension of songs, through audio features, and their lyrics, by a sentiment analysis approach.

The process to obtain data has been developed in base to three powerful resources: the Spotify and Genius APIs, from which we obtained Playlist and lyrics information respectively (1)(2).

Also, a supervised Machine Learning model has been developed to detect and classify the musical genre of Playlist's songs according to audio features and thus add value to the information provided by the two mentioned APIs.

---

## Table of Contents

1. Credentials
2. Response
3. Track Items
4. Genre Classifier
5. SQL Connection and Queries
6. Tableau Visualizations

---
## Credentials

The first step is to set the credentials to access both Spotify and Genius APIs. User client_id and client_secret should be stored in a .env document as id and secret. Once dotenv is loaded, spotifyToken, geniusToken and query_header functions can run smoothly to create the needed tokens (and refresh them in case they expire) to make queries in both APIs.

---

## Response

Once credentials are set and a Playlist link has been passed, the app is set to make the first query to Spotify API. This query should get a successful response with all information contained in a Spotify Playlist, e.g. tracks, artists, addition dates, followers, contributors, etc. In the next step, we will process the response to get only track related data.

---


## Track Items

Response processing has three steps.

### 1. Track related data from response
First, we create a dictionary with the first relevant data; Name, Artist, Song ID and Popularity. We set this data as keys, and values are the corresponding data for the number of songs in the Playlist.

### 2. Audio features
Another query to the Spotify API is made, now with a different endpoint specific for audio features. To get those attributes, we query for each song by iterating the Song ID obtained in the previous step (the ID must be included in the endpoint). More on this, we add the result for each audio attribute as a key, value pair in the existing dictionary, being the attribute the key, and the list of scores for each song the value.

### 3. Lyrics and sentiment analysis
The last part of this process gets new data, in this case from the Genius API. We pass each song name and artist (already included in the dictionary) as arguments for the Genius query, and it looks for coincidences in their database. It needs some time to provide all lyrics, but it is a valuable input for the analysis. To end with this part, a sentiment analysis is carried out on each lyrics, and results are appended into the dictionary, which is now converted into DataFrame.

---

## Genre Classifier

This stage of the project was the most interesting to me. It was an opportunity to start practicing on supervised Machine Learning.

The objective was to classify all songs from the DataFrame by genre. Before that, we got a file from Kaggle (3) conformed by +6000 songs with their audio features, in the same form as Spotify audio attributes' API. Actually, the sample of songs was diverse in terms of chronology and genre, making it very suitable to be used as a training set for the model.

After a few modifications to match audio attributes' names in our DataFrame with Kaggle's, we started the training. The library used has been Sklearn, and we have tested some Random Forest Classifiers to obtain the most accurate parameters. After that, we predicted the test dataset and obtained an accuracy close to 0.50.

The last phase was to use the model in our DataFrame and append the prediction to it. The results were quite realistic: the model proved reliable in genres such as rap or hip-hop, as well as most of pop songs. However, it classified some others as latin in an erroneous way. However, I am satisfied with this Machine Learning test overall.

---


## SQL Connection and Queries

With the completed DataFrame, it is time to set a connection to MySQL Workbench in order to save the results and make them available for anyone with access to the database.

We created the connection with SQL alchemy and created a new database named Spotify, to save any resulting table after completing the whole process for any Playlist. In this case, we stored the table of Today's Top Hits Playlist. Having finished this step, we close the data processing chapter and we dive into presenting the insights of this particular Playlist.

To present data in a visual way, we have made some queries to the table stored in Workbench, and exported the results to Tableau, from where we developed some visualizations and stories.

---

## Tableau Visualizations

### Relevant audio features per genre.

https://public.tableau.com/app/profile/gerard.rius/viz/Relevantaudiofeaturesbygenre/Historia1


### Genre popularity and sentiment.

https://public.tableau.com/app/profile/gerard.rius/viz/Genrepopularityandsentiment/Historia2?publish=yes


### Artist relevance, popularity and sentiment.

https://public.tableau.com/app/profile/gerard.rius/viz/Artistrelevancepopularityandsentimentanalysis/Historia3

--- 

Note: in main.ipynb, any Playlist link can be used to conduct the analysis. Next steps for the project include a functionality that suggests tracks within the playlist according to sentiment and/or desired genre.

---

## Data sources

Spotify Developer API (1)

https://developer.spotify.com/documentation/web-api/

Genius API (2)

https://genius.com/api-clients

Kaggle Audio Features and Genre (3)

(https://www.kaggle.com/datasets/naoh1092/spotify-genre-audio-features)