"""
data_loader.py

Responsible for loading the raw Spotify dataset and cleaning it
into a format ready for similarity computation.
"""

import pandas as pd

# These are the audio features we'll use to compare songs.
# Adjust this list based on what columns your actual dataset has.
FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]


def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load the dataset from a CSV file.

    TODO:
    - Read the CSV using pandas (pd.read_csv)
    - Print the shape and column names so you can sanity-check the data
    - Return the raw DataFrame
    """
    raise NotImplementedError


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset so it's ready for feature extraction.

    TODO:
    - Drop rows with missing values in FEATURE_COLUMNS or 'track_name'
      (hint: df.dropna(subset=...))
    - Drop duplicate songs (hint: df.drop_duplicates(subset='track_name'))
    - Reset the index after dropping rows (df.reset_index(drop=True))
    - Return the cleaned DataFrame
    """
    raise NotImplementedError


def get_feature_matrix(df: pd.DataFrame):
    """
    Extract just the numeric feature columns used for similarity computation.

    TODO:
    - Select FEATURE_COLUMNS from df
    - Return as a numpy array (df[FEATURE_COLUMNS].values)
    """
    raise NotImplementedError
