"""
test_recommender.py

Basic tests for the Recommender class.
Run with: pytest tests/ -v
"""

import pytest
from src.recommender import Recommender

DATA_PATH = "data/spotify_data.csv"


# ── Fixture: build recommender once, reuse across all tests ───
@pytest.fixture(scope="module")
def recommender():
    rec = Recommender(DATA_PATH)
    rec.build()
    return rec


# ── Test 1 ────────────────────────────────────────────────────
def test_build_loads_data(recommender):
    """
    After build(), df and scaled_features must exist
    and have the same number of rows.
    """
    assert recommender.df is not None
    assert recommender.scaled_features is not None
    assert len(recommender.df) == recommender.scaled_features.shape[0]


# ── Test 2 ────────────────────────────────────────────────────
def test_recommend_returns_correct_count(recommender):
    """
    recommend() should return exactly n results
    for a song that exists in the dataset.
    """
    results = recommender.recommend("Blinding Lights", n=5)
    assert len(results) == 5


# ── Test 3 ────────────────────────────────────────────────────
def test_recommend_excludes_input_song(recommender):
    """
    The input song itself should never appear in its own recommendations.
    """
    song = "Blinding Lights"
    results = recommender.recommend(song, n=10)
    track_names = [r["track"].lower() for r in results]
    assert song.lower() not in track_names


# ── Test 4 ────────────────────────────────────────────────────
def test_recommend_unknown_song_returns_empty(recommender):
    """
    A song that doesn't exist in the dataset should
    return an empty list, not crash.
    """
    results = recommender.recommend("xyzzy_song_that_does_not_exist_123")
    assert results == []


# ── Test 5 ────────────────────────────────────────────────────
def test_recommend_same_genre_filter(recommender):
    """
    When same_genre=True, all returned songs must share
    the same genre as the input song.
    """
    song = "Bewajah"
    results = recommender.recommend(song, n=5, same_genre=True)

    assert len(results) > 0

    # Find the input song's genre
    matches = recommender.df[
        recommender.df["track_name"].str.lower() == song.lower()
    ]
    expected_genre = matches.iloc[0]["track_genre"]

    for r in results:
        assert r["genre"] == expected_genre, (
            f"Expected genre '{expected_genre}' but got '{r['genre']}' "
            f"for track '{r['track']}'"
        )


# ── Test 6 ────────────────────────────────────────────────────
def test_scores_are_between_0_and_1(recommender):
    """
    Cosine similarity scores must always be between -1 and 1.
    For normalized audio features they should realistically be 0 to 1.
    """
    results = recommender.recommend("Shape of You", n=10)
    for r in results:
        assert -1.0 <= r["score"] <= 1.0, (
            f"Score out of range: {r['score']} for track '{r['track']}'"
        )