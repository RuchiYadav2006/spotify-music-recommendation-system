"""
recommender.py

Core recommendation logic: builds a similarity matrix from song features
and returns the most similar songs to a given input song.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from src.data_loader import load_data, clean_data, get_feature_matrix


class Recommender:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df: pd.DataFrame | None = None
        self.similarity_matrix: np.ndarray | None = None

    def build(self):
        """
        Build the recommender: load data, clean it, scale features,
        and compute the similarity matrix.

        TODO:
        1. df = load_data(self.csv_path)
        2. df = clean_data(df)
        3. features = get_feature_matrix(df)
        4. Scale features using StandardScaler (important! without this,
           'tempo' [values ~100s] will dominate over 'danceability' [values 0-1])
        5. Compute cosine_similarity(scaled_features) -> self.similarity_matrix
        6. Store the cleaned df as self.df
        """
        raise NotImplementedError

    def recommend(self, song_name: str, n: int = 5) -> list[str]:
        """
        Return the top-n songs most similar to `song_name`.

        TODO:
        1. Find the row index of `song_name` in self.df
           (hint: self.df[self.df['track_name'] == song_name].index)
           - Handle the case where the song isn't found (return empty list
             or raise a clear error)
        2. Get that song's similarity scores: self.similarity_matrix[idx]
        3. Sort scores descending, but SKIP the song itself (it'll have
           similarity 1.0 with itself)
        4. Take the top n indices and map them back to track names
        5. Return as a list of song names
        """
        raise NotImplementedError
