# Project Structure — File by File

```
spotify-recommender/
├── README.md                  ← project overview, setup steps, example usage
├── requirements.txt           ← all Python dependencies with minimum versions
├── .gitignore                 ← tells git what NOT to track (venv/, data CSVs, __pycache__)
│
├── data/
│   ├── .gitkeep               ← empty placeholder so git tracks the folder (CSVs are gitignored)
│   └── spotify_data.csv       ← download from Kaggle, place here (not committed to git)
│
├── src/
│   ├── __init__.py            ← makes src/ a Python package so imports work (e.g. from src.recommender import ...)
│   ├── data_loader.py         ← load CSV, clean rows, extract feature matrix
│   ├── recommender.py         ← build similarity matrix, run recommend()
│   └── app.py                 ← entry point: CLI or Streamlit UI
│
├── tests/
│   ├── __init__.py
│   └── test_recommender.py    ← unit tests (run with: pytest tests/)
│
└── docs/
    ├── how_it_works.md        ← full technical explanation of the pipeline
    ├── project_structure.md   ← this file
    └── design_decisions.md    ← why we made specific choices (cosine vs euclidean, etc.)
```

---

## Why this structure?

### `src/` instead of putting everything in root
Keeps source code separate from config files (README, requirements.txt).
Also makes imports clean — `from src.data_loader import load_data` makes it
immediately obvious where that function lives.

### Separate `data_loader.py`, `recommender.py`, `app.py`
Each file has **one responsibility** (Single Responsibility Principle):
- `data_loader.py` — only knows how to load and clean data
- `recommender.py` — only knows how to build similarity and recommend
- `app.py` — only knows how to talk to the user (CLI / UI)

This means if you want to swap the dataset, you only change `data_loader.py`.
If you want to change the recommendation algorithm, you only change `recommender.py`.
Nothing else breaks.

### `data/` folder is gitignored
Large CSV files (114,000 rows) don't belong in a git repo — they make cloning
slow and bloat the history. We gitignore `*.csv` and document the download
source in the README instead. The `.gitkeep` file ensures the empty `data/`
folder still appears in the repo so a new user knows where to put the file.

### `requirements.txt` with version pins
`pandas>=2.0.0` instead of just `pandas` means anyone cloning your repo can
reproduce your exact environment. Without version pins, the same `pip install`
command could produce different library versions on different machines.

### `docs/` folder
README is for quick orientation. `docs/` is for depth — technical explanations,
design decisions, and architecture notes that would make README too long.
Recruiters and collaborators who want to understand your thinking can go deeper here.

