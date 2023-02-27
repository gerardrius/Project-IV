import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib

def model_data (path):
    '''
    Function that imports the dataframe containing songs' audio features, classified by genre, to be used to train the model.
    Takes the file path as argument and
    Returns a dataframe with the columns
    '''
    # Read excel since the actual file is a '.xlsx'. 
    df = pd.read_excel(path)

    # We maintain the useful data only, some track items and the actual audio features.
    try:
        df = df[['Genre', 'Title', 'Artist', 'popularity', 'id', 'danceability', 'energy',
       'key', 'loudness', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence', 'tempo']]
    except:
        return 'This dataframe does not contain enough audio features information!'

    # Rename columns to match audio features in the dataframe obtained through Spotify API.
    df.rename(columns = {'Title':'Name', 'popularity': 'Popularity', 'id':'Song ID', 'danceability':'Danceability', 
                                     'energy': 'Energy', 'key':'Key', 'loudness':'Loudness', 'mode':'Mode', 'speechiness':'Speechiness', 
                                     'acousticness':'Acousticness', 'instrumentalness':'Instrumentalness', 'liveness':'Liveness',
                                     'valence':'Valence', 'tempo':'Tempo'}, inplace = True)
    
    return df


# from sklearn.model_selection import train_test_split
# data to be used in the model will be
def get_rfc (data):
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

    features = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo']

    train_features = train_data[features]
    train_target = train_data['Genre']

    test_features = test_data[features]
    test_target = test_data['Genre']

    # from sklearn.model_selection import GridSearchCV
    # Define the parameter grid to search
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 20, None],
        'max_features': ['sqrt', 'log2']
    }

    # Initialize a random forest classifier
    # from sklearn.ensemble import RandomForestClassifier
    rfc = RandomForestClassifier()

    # Perform a grid search to find the best hyperparameters
    grid_search = GridSearchCV(rfc, param_grid, cv=5)
    grid_search.fit(train_features, train_target)

    # Print the best hyperparameters and the corresponding accuracy
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Accuracy: {grid_search.best_score_}")

    # import joblib
    rfc = RandomForestClassifier(n_estimators = grid_search.best_params_['n_estimators'], max_depth = grid_search.best_params_['max_depth'], max_features = grid_search.best_params_['max_features'])
    rfc.fit(train_features, train_target)
    joblib.dump(rfc, 'new_genre_mode_spotify_project')

    rfc = joblib.load('new_genre_mode_spotify_project')
    return rfc

# Prepare the new data
# df_audio_features = df[features] WITH THE ACTUAL DF CONTAINING THE WHOLE INFO

# Make predictions on the new data
def genre_predictor (df, r_f_c):
    features = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo']
    df = df[features]
    predictions = r_f_c.predict(df)
    return predictions

def df_append_genre (df, prediction):
    df['Genre'] = prediction
    df['Genre'] = df['Genre'].apply(lambda x: x.capitalize())
    return df