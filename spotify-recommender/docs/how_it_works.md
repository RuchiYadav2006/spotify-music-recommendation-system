# How It Works — Technical Deep Dive

This document explains the full recommendation pipeline step by step,
including *what* each part does and *why* it's done that way.

---

## The Big Picture

```
```
Raw CSV (114,000 rows)
        │
        ▼
   load_data()             ← read CSV into a DataFrame
        │
        ▼
   clean_data()            ← drop nulls, drop duplicate song names, reset index
        │
        ▼
get_feature_matrix()       ← extract 9 numeric audio feature columns as numpy array
        │
        ▼
  StandardScaler()         ← normalize features so no single feature dominates
        │
        ▼
  recommend(song, n)       ← compute on-demand cosine similarity for queried song
        │
        ├── same_genre=False → return top-N across all 73,608 songs
        │
        └── same_genre=True  → filter to same genre first, then return top-N
```
```

---

## Step 1 — Loading the Data (`load_data`)

```python
df = pd.read_csv(csv_path)
```

Reads the Kaggle Spotify Tracks dataset (114,000 rows × 21 columns) into a
pandas DataFrame. Kept as its own function so switching data sources later
(different CSV, an API, a database) only requires changing one place.

---

## Step 2 — Cleaning the Data (`clean_data`)

Three operations, each for a specific reason:

### Drop rows with missing feature values
```python
df = df.dropna(subset=FEATURE_COLUMNS + ["track_name"])
```
A missing `tempo` or `danceability` value would produce a garbage similarity
score. We remove those rows entirely rather than guessing/filling values.

### Drop duplicate song names
```python
df = df.drop_duplicates(subset="track_name")
```
This dataset lists the same song under multiple genres
(e.g. "Blinding Lights" appears under pop, dance, and electronic separately).
Keeping duplicates means the same song would show up multiple times in
recommendations. We keep only the first occurrence per track name.

### Reset the index
```python
df = df.reset_index(drop=True)
```
After dropping rows, the DataFrame index has gaps (0, 1, 5, 9...).
We reset it to a clean 0,1,2,3... sequence because the similarity matrix
uses row positions as array indices — gaps would cause wrong song lookups.

**Result: 73,608 unique songs ready for processing.**

---

## Step 3 — Feature Selection

```python
FEATURE_COLUMNS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo"
]
```

These 9 columns are Spotify's audio analysis features. They describe the
musical character of a track — not metadata like artist name or genre.
This means the recommender can find similar-sounding songs across genres,
which is more interesting than just "other pop songs."

Columns we deliberately exclude:
| Column | Reason excluded |
|---|---|
| `track_name`, `artists`, `album_name` | Metadata, not sound |
| `track_genre` | Would bias toward same-genre only |
| `popularity` | Measures fame, not musical similarity |
| `duration_ms`, `key`, `mode`, `time_signature` | Low signal for perceptual similarity |

---

## Step 4 — Feature Scaling (`StandardScaler`)

```python
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
```

**This is the most important step people skip.**

Look at the raw value ranges before scaling:

| Feature | Typical range |
|---|---|
| `tempo` | 60 – 200 |
| `loudness` | -60 – 0 |
| `danceability` | 0.0 – 1.0 |
| `acousticness` | 0.0 – 1.0 |

Without scaling, `tempo` (values ~60–200) would dominate the similarity
calculation because its numbers are ~100× larger than danceability (0–1).
Two songs could have completely different energy, mood, and acoustic character
but get called "similar" just because their tempos are close.

`StandardScaler` converts every feature to **mean = 0, standard deviation = 1**.
Now all 9 features contribute equally to the similarity score.

---

## Step 5 — Cosine Similarity

```python
self.similarity_matrix = cosine_similarity(scaled_features)
```

**What it measures:** the angle between two feature vectors, not their
Euclidean distance. Two songs are similar if their audio feature vectors
point in the same direction, regardless of magnitude.

**Output:** a matrix of shape `(73608 × 73608)` — every song compared to
every other song. Each cell contains a score from -1 to 1:

| Score | Meaning |
|---|---|
| 1.0 | Identical direction — the song itself |
| 0.8–0.99 | Very similar |
| 0.5–0.8 | Somewhat similar |
| < 0.5 | Quite different |

**Why cosine and not Euclidean distance?** Euclidean distance cares about
magnitude — a very loud, high-energy song and a quieter version of the same
style would appear "far apart." Cosine similarity only cares about the
pattern/direction of features, which better captures musical style.

---

## Step 6 — Recommendation (`recommend`)

```python
def recommend(self, song_name: str, n: int = 5) -> list:
    idx = matches.index[0]                              # find song's row
    scores = sorted(enumerate(self.similarity_matrix[idx]),
                    key=lambda x: x[1], reverse=True)  # sort all scores
    top_n = scores[1:n + 1]                            # skip index 0 (itself)
```

Given a song name:
1. Find its row index in the DataFrame using a case-insensitive match
2. Pull that song's row from the similarity matrix (73,608 scores)
3. Sort all scores descending
4. Skip position 0 — the song always has a perfect score of 1.0 with itself
5. Return the top-N results with track name, artist, and similarity score

---

## Example Output

```
Input: "Blinding Lights"

Results:
  Save Your Tears      – The Weeknd      (score: 0.987)
  In Your Eyes         – The Weeknd      (score: 0.981)
  Levitating           – Dua Lipa        (score: 0.974)
  Don't Start Now      – Dua Lipa        (score: 0.969)
  Physical             – Dua Lipa        (score: 0.961)
```

Notice: the recommender found Dua Lipa songs as similar to The Weeknd —
not because they're the same artist, but because their audio features
(high energy, high danceability, similar tempo) are numerically close.
That's the power of content-based filtering.
