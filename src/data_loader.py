import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATINGS_PATH = os.path.join(BASE_DIR, "data", "ratings.csv")
MOVIES_PATH  = os.path.join(BASE_DIR, "data", "movies.csv")


def load_ratings() -> pd.DataFrame:
    """Load the ratings CSV and return a clean DataFrame."""
    df = pd.read_csv(RATINGS_PATH)
    df["user_id"]  = df["user_id"].astype(str)
    df["movie_id"] = df["movie_id"].astype(int)
    df["rating"]   = df["rating"].astype(float)
    return df


def load_movies() -> pd.DataFrame:
    """Load the movies CSV and return a clean DataFrame."""
    df = pd.read_csv(MOVIES_PATH)
    df["movie_id"] = df["movie_id"].astype(int)
    return df


def build_user_item_matrix(ratings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot the ratings DataFrame into a User-Item Matrix.
    Rows = users, Columns = movie_ids, Values = ratings (NaN for unrated).
    """
    matrix = ratings_df.pivot_table(
        index="user_id",
        columns="movie_id",
        values="rating"
    )
    return matrix


def get_movie_details(movie_id: int, movies_df: pd.DataFrame) -> dict:
    """Return a dict of movie details for a given movie_id."""
    row = movies_df[movies_df["movie_id"] == movie_id]
    if row.empty:
        return {}
    return row.iloc[0].to_dict()
