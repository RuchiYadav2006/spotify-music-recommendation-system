# Spotify Song Recommender (Content-Based)

A content-based music recommendation engine that suggests similar songs based on audio
features (danceability, energy, tempo, acousticness, etc.) using cosine similarity.

> Status: 🚧 In progress — built step-by-step as a learning project.

## How it works

1. Load a dataset of songs with their audio features.
2. Normalize the numeric features so no single feature (like tempo, which has large values)
   dominates the similarity calculation.
3. Compute pairwise cosine similarity between all songs based on their feature vectors.
4. Given a song name, return the top-N most similar songs.

## Project structure

```
spotify-recommender/
├── README.md
├── requirements.txt
├── .gitignore
├── data/                   # dataset goes here (not committed to git)
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # loads & cleans the dataset
│   ├── recommender.py      # builds similarity matrix, returns recommendations
│   └── app.py              # CLI / Streamlit entry point
└── tests/
    └── test_recommender.py
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the dataset (see Data section below) into data/

# 4. Run it
python -m src.app
```

## Data

Dataset: [Spotify Tracks Dataset on Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
(or similar — any Spotify audio-features CSV works).

Place the CSV in `data/spotify_data.csv`.

## Tech stack

- Python, pandas, scikit-learn (cosine similarity, StandardScaler)
- Streamlit (optional simple UI)

## Example usage

```python
from src.recommender import Recommender

rec = Recommender("data/spotify_data.csv")
rec.build()
print(rec.recommend("Blinding Lights", n=5))
```

## Future improvements

- Add collaborative filtering using user listening history
- Deploy as a web app
- Add genre-based filtering on top of audio-feature similarity

## Resume bullet (draft — to finalize once built)

> Built a content-based music recommendation engine in Python using cosine similarity
> on normalized Spotify audio features, returning top-N similar tracks for any given song.
