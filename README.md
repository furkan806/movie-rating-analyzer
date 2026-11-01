# Movie Rating Analyzer

A small Python 3 console project that reads movie ratings from CSV, skips invalid rows, removes exact duplicates, summarizes ratings, groups ratings by genre, and displays Matplotlib charts.

## Requirements

- Python 3.10 or newer
- The packages in `requirements.txt`

## Run

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python movie_rating_analyzer.py
```

Running the script uses `data/movies.csv` automatically. To use another file, pass its path as an argument, for example `python movie_rating_analyzer.py path/to/movies.csv`. The CSV must have `Movie`, `Genre`, and `Rating` columns. Ratings must be numeric values from 0 through 10.

Menu options show a summary, genre averages with a bar chart, both the bar chart and rating histogram, or exit. Invalid or incomplete rows are reported and skipped; exact duplicate records are removed.
