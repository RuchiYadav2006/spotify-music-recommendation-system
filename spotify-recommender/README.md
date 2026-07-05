# Spotify Song Recommender (Content-Based)

A content-based music recommendation engine that suggests similar songs based on audio
features (danceability, energy, tempo, acousticness, etc.) using cosine similarity.

> Status: 🚧 In progress — built step-by-step as a learning project.

---

## How it works

```
Raw CSV (114,000 rows)  →  clean & deduplicate  →  scale features
→  cosine similarity matrix  →  recommend(song, n)  →  top-N results
```

1. Load 114,000 Spotify tracks with their audio features
2. Remove duplicates and nulls → 73,608 unique songs
3. Normalize features with `StandardScaler` so tempo doesn't dominate danceability
4. Compute pairwise cosine similarity across all 73,608 songs
5. Given any song name, return the top-N most similar tracks

📖 **Full technical explanation:** [docs/how_it_works.md](docs/how_it_works.md)

---

## Project structure

```
spotify-recommender/
├── README.md
├── requirements.txt
├── .gitignore
├── data/                        # dataset goes here (not committed to git)
├── src/
│   ├── __init__.py
│   ├── data_loader.py           # loads & cleans the dataset
│   ├── recommender.py           # builds similarity matrix, returns recommendations
│   └── app.py                   # CLI / Streamlit entry point
├── tests/
│   └── test_recommender.py
└── docs/
    ├── how_it_works.md          # full pipeline explanation with visuals
    ├── project_structure.md     # what every file does and why
    └── design_decisions.md      # key technical tradeoffs explained
```

📖 **File-by-file breakdown:** [docs/project_structure.md](docs/project_structure.md)

---

## Setup

```bash
# create + activate a venv
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install deps
pip install -r requirements.txt

# grab the dataset from Kaggle and drop it in data/spotify_data.csv
# https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

# run it
python -m src.app
# or, for the web UI:
streamlit run streamlit_app.py
```


## Dataset

[Spotify Tracks Dataset — Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

- 114,000 tracks × 21 columns
- 73,608 unique songs after deduplication
- Place the CSV at `data/spotify_data.csv` (gitignored — not committed)

---

## Tech stack

| Library | Used for |
|---|---|
| `pandas` | Loading and cleaning the dataset |
| `scikit-learn` | StandardScaler (feature normalization), cosine_similarity |
| `numpy` | Similarity matrix operations |
| `streamlit` | Optional interactive UI |

---

## Example usage

```python
from src.recommender import Recommender

rec = Recommender("data/spotify_data.csv")
rec.build()

results = rec.recommend("Blinding Lights", n=5)
for r in results:
    print(r)
```

**Output:**
```
{'track': 'Save Your Tears',  'artist': 'The Weeknd', 'score': 0.987}
{'track': 'Levitating',       'artist': 'Dua Lipa',   'score': 0.974}
{'track': "Don't Start Now",  'artist': 'Dua Lipa',   'score': 0.969}
```

---

## Key design decisions

- **Content-based over collaborative filtering** — no user history needed; works on audio features alone
- **Cosine similarity over Euclidean distance** — captures musical style, not just raw magnitude
- **StandardScaler before similarity** — prevents high-range features (tempo) from dominating low-range ones (danceability)

📖 **Full reasoning:** [docs/design_decisions.md](docs/design_decisions.md)

---

## Things I'd add if I kept going

- Approximate nearest neighbor search (Faiss/Annoy) so it scales past 73k songs
  without recomputing similarity from scratch each time
- Deploy the Streamlit app somewhere (Streamlit Cloud / HF Spaces)
- Maybe a hybrid model down the line if I can find a dataset with listening
  history attached

