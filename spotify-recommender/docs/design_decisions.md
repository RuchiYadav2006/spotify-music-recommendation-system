# Design Decisions

Every project involves tradeoffs. This document explains the key choices made
and why — the kind of things you'd discuss in a technical interview.

---

## Why content-based filtering, not collaborative filtering?

| Approach | How it works | Needs |
|---|---|---|
| **Content-based** (what we built) | Compare audio features of songs | Just the song data |
| **Collaborative filtering** | "Users who liked X also liked Y" | User listening history |

We chose content-based because:
- The Kaggle dataset has no user listening history — only song features
- Content-based is explainable: "these songs are similar because their energy, tempo, and danceability are close"
- No cold-start problem: works for any song in the dataset, even unpopular ones

---

## Why cosine similarity, not Euclidean distance?

Both measure how "close" two feature vectors are, but differently.

**Euclidean distance** measures the straight-line distance between two points.
Problem: a very loud, high-energy song and a slightly quieter version of the
same style would appear "far apart" even though they sound similar.

**Cosine similarity** measures the angle between vectors — not their magnitude.
Two songs are similar if their feature patterns point in the same direction,
regardless of absolute values. This better captures musical style.

Example: song A has features [0.8, 0.9, 0.7] and song B has [0.4, 0.45, 0.35].
Euclidean sees them as different. Cosine sees them as near-identical
(same ratio of features — just different "volume").

---

## Why StandardScaler before computing similarity?

Raw feature ranges are wildly different:

| Feature | Range |
|---|---|
| tempo | 60 – 200 |
| loudness | -60 – 0 |
| danceability | 0.0 – 1.0 |

Without scaling, `tempo` dominates the similarity score because its values
are 100× larger than danceability. Two songs with identical mood, energy,
and acoustic character but slightly different tempos would appear "dissimilar."

`StandardScaler` normalizes every feature to mean=0, std=1 so all 9 features
contribute equally to the final similarity score.

---

## Why drop duplicate track names?

The dataset contains the same song listed multiple times under different genres.
"Blinding Lights" appears under pop, dance, and electronic as separate rows.

If we keep duplicates:
- The similarity matrix grows unnecessarily (slower, more memory)
- Recommendations could return the same song multiple times under different entries
- `recommend()` would return the first match — but which duplicate? Unpredictable.

Dropping to one entry per track name keeps results clean and deterministic.

---

## Why precompute the full similarity matrix in `build()`?

Alternative: compute similarity on-the-fly at query time (only for the queried song).

| Approach | Query speed | Memory | Build time |
|---|---|---|---|
| Precompute full matrix | Instant (just an array lookup) | ~43 GB for 73k songs... wait |
| Compute at query time | ~0.5s per query | Very low | None |

**Wait — 43 GB?** A 73,608 × 73,608 float64 matrix would be ~43 GB.
That's clearly not what we're building here. In practice, scikit-learn's
`cosine_similarity` for 73k songs takes ~10–30 seconds and uses ~1–2 GB RAM
depending on your machine — manageable for a local project and demo.

For a production system you would:
- Use approximate nearest neighbor search (Faiss, Annoy)
- Precompute and store to disk
- Only compute similarity for the queried song at runtime

For a portfolio mini-project, full precomputation is fine and simpler to explain.

---

## Why CLI first, Streamlit second?

Command-line first because:
- Forces you to make the logic completely separate from the UI
- Easier to test (just call the function, no browser needed)
- If the CLI works, Streamlit is just a wrapper — very fast to add

Building UI first often leads to logic tangled inside UI code, which is
harder to test and harder to change later.



## Why on-demand similarity instead of precomputing the full matrix?

First attempt used `cosine_similarity(all_73k_songs)` which tries to allocate
a 73,608 × 73,608 float64 matrix — that's **40.4 GB of RAM**. Crashed
immediately on a normal laptop with `numpy.core.exceptions.ArrayMemoryError`.

Fix: compute similarity only for the queried song at query time:

| Approach | Memory | Query speed |
|---|---|---|
| Precompute full matrix | 40.4 GB ❌ | Instant |
| On-demand (what we use) | ~0.6 MB ✅ | ~0.5s per query |

```python
# Instead of this (40 GB):
self.similarity_matrix = cosine_similarity(scaled_features)

# We do this (0.6 MB):
song_vector = self.scaled_features[idx].reshape(1, -1)
scores = cosine_similarity(song_vector, self.scaled_features)[0]
```

For a production system with millions of songs you'd use approximate nearest
neighbor search (Faiss, Annoy) instead — but on-demand cosine is perfectly
fast for a 73k-song portfolio project.


## Why add a same-genre filter on top of cosine similarity?

Pure audio-feature similarity is language and culture blind. The model only
sees 9 numbers per song — it has no concept of Hindi, Portuguese, or English.

**The problem we hit:**
Searching "Tu Hi Haqeeqat" (Bollywood ballad) returned Brazilian/Portuguese
songs — not because the algorithm was wrong, but because those songs had
nearly identical audio profiles (soft, acoustic, low energy, low tempo).

**The fix:**
Added an optional `same_genre` flag to `recommend()`:

```python
def recommend(self, song_name: str, n: int = 5, same_genre: bool = False)
```

When `same_genre=True`:
- Find the input song's `track_genre` from the dataset
- During result collection, skip any song whose genre doesn't match
- Show which genre is being filtered in the UI

**Why optional and not always on?**
Sometimes cross-genre discovery is the point — "Blinding Lights" (pop)
legitimately shares audio DNA with certain electronic or dance tracks.
Forcing same-genre always would kill those interesting cross-genre finds.
Giving the user a toggle lets them choose based on what they want.

**Limitation that remains:**
The dataset's genre labels are