"""
test_recommender.py

Basic tests for the recommender. Run with: pytest tests/
"""

import pytest
from src.recommender import Recommender

DATA_PATH = "data/spotify_data.csv"


def test_build_creates_similarity_matrix():
    """
    TODO:
    - Create a Recommender(DATA_PATH), call .build()
    - Assert that rec.similarity_matrix is not None
    - Assert that rec.similarity_matrix.shape[0] == rec.similarity_matrix.shape[1]
      (it should be a square matrix: song x song)
    """
    pass


def test_recommend_returns_n_songs():
    """
    TODO:
    - Build the recommender
    - Pick a song name that you know exists in your dataset
    - Call rec.recommend(song_name, n=5)
    - Assert len(result) == 5
    - Assert the input song itself is NOT in the result list
    """
    pass


def test_recommend_unknown_song_handled_gracefully():
    """
    TODO:
    - Call rec.recommend("some song that definitely doesn't exist")
    - Assert it doesn't crash — either returns [] or raises a clear,
      catchable exception (your choice, just be intentional about it)
    """
    pass
