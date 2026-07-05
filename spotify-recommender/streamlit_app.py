"""
streamlit_app.py

Streamlit UI for the Spotify Song Recommender.
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
from src.recommender import Recommender

# ─>-- Page config --<--
st.set_page_config(
    page_title="Spotify Song Recommender",
    page_icon="🎵",
    layout="centered"
)

# ─>-- Load recommender once (cached so it doesn't reload on every interaction) ─<--
@st.cache_resource
def load_recommender():
    rec = Recommender("data/spotify_data.csv")
    rec.build()
    return rec

# ─>-- Header ─<--
st.title("🎵 Spotify Song Recommender")
st.markdown(
    "Enter a song name and get similar tracks based on audio features "
    "like energy, danceability, tempo, and acousticness."
)
st.divider()

# ─>-- Load model ─<--
with st.spinner("Loading recommender (first load takes a few seconds)..."):
    rec = load_recommender()

st.success("Recommender ready!", icon="✅")

# ─>-- Input ─<--
st.subheader("Search")
song_name = st.text_input(
    label="Song name",
    placeholder="e.g. Tu Hi Haqeeqat, Blinding Lights, Shape of You"
)
n = st.slider("Number of recommendations", min_value=1, max_value=10, value=5)

same_genre = st.toggle(
    "🎸 Same genre only",
    value=False,
    help="Restrict recommendations to songs from the same genre as the input song."
)

# ─>-- Recommend ──<--
if st.button("Recommend 🎧", use_container_width=True):
    if not song_name.strip():
        st.warning("Please enter a song name.")
    else:
        with st.spinner(f"Finding songs similar to '{song_name}'..."):
            results = rec.recommend(song_name.strip(), n=n, same_genre=same_genre)

        if not results:
            st.error(
                f"**'{song_name}'** not found in the dataset. "
                "Try checking the spelling or use a different song."
            )
        else:
            # Show which genre was used if filter is on
            if same_genre:
                st.info(f"🎸 Filtering by genre: **{results[0]['genre']}**")

            st.subheader(f"Top {len(results)} songs similar to '{song_name}'")

            for i, r in enumerate(results, 1):
                with st.container():
                    col1, col2, col3 = st.columns([0.5, 3.5, 0.8])
                    col1.markdown(f"**{i}**")
                    col2.markdown(f"**{r['track']}** — *{r['artist']}*  \n`{r['genre']}`")
                    col3.markdown(f"`{r['score']}`")
                st.divider()

# ─>-- Footer ──<--

st.markdown(
    """
    ---
    **How it works:** audio features are normalized with `StandardScaler`,
    then cosine similarity is computed on-demand between the queried song
    and all 73,608 tracks in the dataset. See `docs/how_it_works.md` for
    the full pipeline.
    """
)