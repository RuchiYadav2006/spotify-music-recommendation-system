# Design Decisions

Notes on the choices I made and why, mostly so I remember my own reasoning
later.


## Why content-based filtering, not collaborative filtering?

The Kaggle dataset only has song-level audio features - no user IDs, no
play counts, nothing about who listened to what. So collaborative filtering
("people who liked X also liked Y") was never really on the table here.
Content-based also has a nice side effect: no cold-start problem, since it
works the same whether the song is a hit or has 12 plays.

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

If I keep duplicates:
- The similarity matrix grows unnecessarily (slower, more memory)
- Recommendations could return the same song multiple times under different entries
- `recommend()` would return the first match — but which duplicate? Unpredictable.

Dropping to one entry per track name keeps results clean and deterministic.

---


## Why CLI first, Streamlit second?

Command-line first because:
- Forces you to make the logic completely separate from the UI
- Easier to test (just call the function, no browser needed)
- If the CLI works, Streamlit is just a wrapper — very fast to add

Building UI first often leads to logic tangled inside UI code, which is
harder to test and harder to change later.



## Computing similarity per-query instead of one big matrix

My first version tried to precompute the whole similarity matrix up front,
figuring I'd just look up a row whenever someone searched a song:

```python
self.similarity_matrix = cosine_similarity(scaled_features)
```

That's a 73,608 x 73,608 matrix of floats, which works out to roughly 40GB
of RAM. It died instantly on my laptop with an `ArrayMemoryError`. Once I
did the math I realized precomputing everything up front never made sense
at this scale - so instead I only compute similarity between the queried
song and everyone else, at query time:

```python
song_vector = self.scaled_features[idx].reshape(1, -1)
scores = cosine_similarity(song_vector, self.scaled_features)[0]
```

That's a fraction of a second per search and a few hundred KB of memory
instead of 40GB. For something with millions of songs you'd want an
approximate nearest-neighbor index (Faiss, Annoy) instead of brute-force
cosine similarity even at query time - but for 73k songs, brute force is
fine.

## Why add a same-genre filter on top of cosine similarity?

Pure audio-feature similarity has no idea what language or culture a song
belongs to - it only sees 9 numbers. I ran into this searching for "Tu Hi
Haqeeqat" (a Bollywood ballad) and getting back Brazilian acoustic tracks,
which isn't wrong exactly - they really do have almost identical tempo,
energy, and acousticness - but it's not a useful recommendation if you
wanted something in the same genre/language.

So `recommend()` takes an optional `same_genre` flag that restricts results
to the same `track_genre` as the input song. It's off by default because
sometimes the cross-genre matches are the interesting part (that's how
"Blinding Lights" ends up next to some electronic/dance tracks it has no
obvious business being near). The genre labels in this dataset aren't
perfectly clean either - the same song can appear under a slightly
different genre tag depending on how it was scraped - so the filter helps
but isn't airtight.