"""
recommender.py

Core recommendation logic.
Computes similarity on-demand for the queried song only.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from src.data_loader import load_data, clean_data, get_feature_matrix


class Recommender:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df: pd.DataFrame = None
        self.scaled_features: np.ndarray = None

    def build(self):
        print("Loading and cleaning data...")
        df = load_data(self.csv_path)
        df = clean_data(df)

        print("Scaling features...")
        features = get_feature_matrix(df)
        scaler = StandardScaler()
        self.scaled_features = scaler.fit_transform(features)

        self.df = df
        print("Recommender ready!")

    def recommend(self, song_name: str, n: int = 5, same_genre: bool = False) -> list:
        if self.df is None or self.scaled_features is None:
            raise RuntimeError("Call build() before recommend()")

        matches = self.df[self.df["track_name"].str.lower() == song_name.lower()]

        if matches.empty:
            print(f"Song '{song_name}' not found in dataset.")
            return []

        idx = matches.index[0]
        genre = self.df.iloc[idx]["track_genre"]

        song_vector = self.scaled_features[idx].reshape(1, -1)
        scores = cosine_similarity(song_vector, self.scaled_features)[0]

        sorted_indices = np.argsort(scores)[::-1]

        results = []
        for i in sorted_indices:
            if i == idx:
                continue

            row = self.df.iloc[i]

            if same_genre and row["track_genre"] != genre:
                continue

            results.append({
                "track": row["track_name"],
                "artist": row["artists"],
                "genre": row["track_genre"],
                "score": round(float(scores[i]), 3)
            })

            if len(results) == n:
                break

        return results