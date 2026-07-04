"""
data_loader.py

Responsible for loading the raw Spotify dataset and cleaning it
into a format ready for similarity computation.
"""

import pandas as pd

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
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=FEATURE_COLUMNS + ["track_name"])
    df = df.drop_duplicates(subset="track_name")
    df = df.reset_index(drop=True)
    print(f"After cleaning: {df.shape[0]} unique songs")
    return df


def get_feature_matrix(df: pd.DataFrame):
    return df[FEATURE_COLUMNS].values