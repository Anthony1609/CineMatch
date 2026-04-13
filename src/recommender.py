import numpy as np
import pandas as pd

from src.similarity import compute_user_similarity_matrix, get_top_n_similar_users
from src.data_loader  import load_ratings, load_movies, build_user_item_matrix


def predict_rating(
    target_user_row: pd.Series,
    movie_id: int,
    similar_users: list[tuple[str, float]],
    user_item_matrix: pd.DataFrame
) -> float:
    """
    Weighted average prediction for how the target user would rate *movie_id*.
    Uses ratings from similar users, weighted by their cosine-similarity score.
    """
    numerator   = 0.0
    denominator = 0.0

    for user_id, sim_score in similar_users:
        if sim_score <= 0:
            continue
        if movie_id not in user_item_matrix.columns:
            continue
        rating = user_item_matrix.loc[user_id, movie_id]
        if np.isnan(rating):
            continue
        numerator   += sim_score * rating
        denominator += sim_score

    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 2)


def get_recommendations(
    user_ratings: dict,          # {movie_id (int): rating (float)}
    top_k: int = 5,
    n_similar_users: int = 3
) -> list[dict]:
    """
    Main recommendation function.

    Parameters
    ----------
    user_ratings : dict
        Ratings submitted by the new/current user  {movie_id: rating}.
    top_k : int
        Number of recommendations to return.
    n_similar_users : int
        How many neighbours to use for prediction.

    Returns
    -------
    List of dicts, each containing movie details + predicted_rating.
    """
    # --- Load data --------------------------------------------------------
    ratings_df      = load_ratings()
    movies_df       = load_movies()
    user_item_matrix = build_user_item_matrix(ratings_df)

    # --- Add the current user as a temporary row --------------------------
    TEMP_ID = "YOU"
    all_movie_ids = user_item_matrix.columns.tolist()

    new_row = {mid: np.nan for mid in all_movie_ids}
    for mid, rating in user_ratings.items():
        if mid in all_movie_ids:
            new_row[mid] = float(rating)

    new_series = pd.Series(new_row, name=TEMP_ID)
    extended_matrix = pd.concat([user_item_matrix, new_series.to_frame().T])

    # --- Compute similarity -----------------------------------------------
    sim_matrix    = compute_user_similarity_matrix(extended_matrix)
    similar_users = get_top_n_similar_users(TEMP_ID, sim_matrix, n=n_similar_users)

    # --- Identify unrated movies for the current user ---------------------
    rated_ids   = set(user_ratings.keys())
    unrated_ids = [mid for mid in all_movie_ids if mid not in rated_ids]

    # --- Predict ratings for every unrated movie --------------------------
    predictions = []
    for movie_id in unrated_ids:
        predicted = predict_rating(
            target_user_row=extended_matrix.loc[TEMP_ID],
            movie_id=movie_id,
            similar_users=similar_users,
            user_item_matrix=extended_matrix
        )
        if predicted > 0:
            movie_row = movies_df[movies_df["movie_id"] == movie_id]
            if not movie_row.empty:
                info = movie_row.iloc[0].to_dict()
                info["predicted_rating"] = predicted
                info["match_pct"]        = min(100, int((predicted / 5.0) * 100))
                predictions.append(info)

    # --- Sort and return top-K -------------------------------------------
    predictions.sort(key=lambda x: x["predicted_rating"], reverse=True)
    return predictions[:top_k]


def get_all_movies() -> list[dict]:
    """Return all movies as a list of dicts (for the rating UI)."""
    movies_df = load_movies()
    return movies_df.to_dict(orient="records")
