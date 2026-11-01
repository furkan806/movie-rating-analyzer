"""Analyze movie ratings from a CSV file and display charts."""

from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = {"Movie", "Genre", "Rating"}


def load_movies(csv_path: Path) -> pd.DataFrame:
    """Load and validate rows, printing a reason for each skipped row."""
    raw = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

    rows = []
    for row_number, row in raw.iterrows():
        line = row_number + 2  # Header is line 1.
        movie, genre, rating_text = (row["Movie"].strip(), row["Genre"].strip(), row["Rating"].strip())
        if not movie or not genre or not rating_text:
            print(f"Row {line} skipped: Movie, Genre, and Rating must not be empty.")
            continue
        try:
            rating = float(rating_text)
        except ValueError:
            print(f"Row {line} skipped: invalid Rating {rating_text!r}.")
            continue
        if not 0 <= rating <= 10:
            print(f"Row {line} skipped: Rating {rating:g} must be between 0 and 10.")
            continue
        rows.append({"Movie": movie, "Genre": genre, "Rating": rating})

    movies = pd.DataFrame(rows, columns=["Movie", "Genre", "Rating"])
    before = len(movies)
    movies = movies.drop_duplicates(subset=["Movie", "Genre", "Rating"])
    if before > len(movies):
        print(f"Removed {before - len(movies)} duplicate row(s).")
    if movies.empty:
        print("Valid rows: 0")
    else:
        print(f"Valid rows: {len(movies)}")
    return movies


def show_summary(movies: pd.DataFrame) -> None:
    if movies.empty:
        print("No valid movie rows to summarize.")
        return
    print(f"Average rating: {movies['Rating'].mean():.2f}")
    highest = movies.loc[movies["Rating"].idxmax()]
    lowest = movies.loc[movies["Rating"].idxmin()]
    print(f"Top rated: {highest['Movie']} ({highest['Rating']:g})")
    print(f"Lowest: {lowest['Movie']} ({lowest['Rating']:g})")


def show_genres(movies: pd.DataFrame) -> None:
    if movies.empty:
        print("No valid movie rows to group by genre.")
        return
    averages = movies.groupby("Genre")["Rating"].mean().sort_values(ascending=False)
    for genre, average in averages.items():
        print(f"{genre}: {average:.2f}")
    print(f"Best genre: {averages.index[0]}")
    averages.plot(kind="bar", color="steelblue", title="Genre-wise Average Rating")
    plt.xlabel("Genre")
    plt.ylabel("Average rating (out of 10)")
    plt.ylim(0, 10)
    plt.tight_layout()
    plt.show()


def show_charts(movies: pd.DataFrame) -> None:
    if movies.empty:
        print("No valid movie rows to chart.")
        return
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    movies.groupby("Genre")["Rating"].mean().sort_values().plot(
        kind="bar", ax=axes[0], color="steelblue", title="Genre-wise Average Rating"
    )
    axes[0].set(xlabel="Genre", ylabel="Average rating (out of 10)", ylim=(0, 10))
    axes[1].hist(movies["Rating"], bins=10, range=(0, 10), color="coral", edgecolor="white")
    axes[1].set(title="Movie Rating Distribution", xlabel="Rating (out of 10)", ylabel="Number of movies")
    fig.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze movie ratings from a CSV file.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        help="CSV file to analyze (defaults to the sample data/movies.csv)",
    )
    args = parser.parse_args()
    default_csv = Path(__file__).parent / "data" / "movies.csv"
    csv_path = args.csv_path.expanduser() if args.csv_path else default_csv
    try:
        movies = load_movies(csv_path)
    except (OSError, pd.errors.ParserError, ValueError) as error:
        print(f"Could not load CSV: {error}")
        return

    while True:
        print("\n1. Summary  2. Genre-wise average  3. Show both charts  4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_summary(movies)
        elif choice == "2":
            show_genres(movies)
        elif choice == "3":
            show_charts(movies)
        elif choice == "4":
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
