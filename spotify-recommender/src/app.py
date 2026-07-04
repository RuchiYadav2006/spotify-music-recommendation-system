"""
app.py

Entry point — runs the recommender as an interactive CLI.
Run with: python -m src.app
"""

from src.recommender import Recommender

DATA_PATH = "data/spotify_data.csv"


def display_results(results: list, song_name: str):
    if not results:
        print(f"\nNo recommendations found for '{song_name}'.")
        return

    print(f"\nTop {len(results)} songs similar to '{song_name}':\n")
    print(f"  {'#':<4} {'Track':<40} {'Artist':<30} {'Score'}")
    print(f"  {'-'*4} {'-'*40} {'-'*30} {'-'*5}")
    for i, r in enumerate(results, 1):
        print(f"  {i:<4} {r['track']:<40} {r['artist']:<30} {r['score']}")


def main():
    print("=" * 60)
    print("       Spotify Song Recommender (Content-Based)")
    print("=" * 60)

    # Build the recommender once — this takes a few seconds
    rec = Recommender(DATA_PATH)
    rec.build()

    print("\nType a song name to get recommendations.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        song_name = input("Enter song name: ").strip()

        if not song_name:
            print("Please enter a song name.")
            continue

        if song_name.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        try:
            results = rec.recommend(song_name, n=5)
            display_results(results, song_name)
        except Exception as e:
            print(f"Error: {e}")

        print()  # blank line between queries


if __name__ == "__main__":
    main()