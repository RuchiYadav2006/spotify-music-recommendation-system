"""
app.py

Entry point to run the recommender from the command line.
Run with: python -m src.app
"""

from src.recommender import Recommender

DATA_PATH = "data/spotify_data.csv"


def main():
    """
    TODO:
    1. Create a Recommender(DATA_PATH) instance
    2. Call .build() on it
    3. Ask the user to input a song name (input("Enter a song name: "))
    4. Call .recommend(song_name) and print the results nicely
    5. (Optional, later) wrap this in a loop so the user can query multiple songs
       without restarting the script
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
