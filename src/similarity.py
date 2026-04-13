import numpy as np
import pandas as pd


def cosine_similarity_vectors(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Compute cosine similarity between two 1-D NumPy arrays.
    Only considers indices where BOTH vectors have valid (non-NaN) values.
    Returns a float in [0, 1], or 0.0 if no common rated items exist.
    """
    mask = ~(np.isnan(vec_a) | np.isnan(vec_b))
    if mask.sum() == 0:
        return 0.0

    a = vec_a[mask]
    b = vec_b[mask]

    dot    = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot / (norm_a * norm_b))


def compute_user_similarity_matrix(user_item_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Build a full (n_users x n_users) cosine-similarity matrix from the
    User-Item Matrix.  Returns a DataFrame indexed and columned by user_id.
    """
    users  = user_item_matrix.index.tolist()
    values = user_item_matrix.values          # raw NumPy array
    n      = len(users)
    sim    = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                sim[i][j] = 1.0
            elif j > i:
                s = cosine_similarity_vectors(values[i], values[j])
                sim[i][j] = s
                sim[j][i] = s                 # matrix is symmetric

    return pd.DataFrame(sim, index=users, columns=users)


def get_top_n_similar_users(
    target_user_id: str,
    similarity_matrix: pd.DataFrame,
    n: int = 3
) -> list[tuple[str, float]]:
    """
    Return the top-N most similar users to *target_user_id*
    as a list of (user_id, similarity_score) tuples, sorted descending.
    The target user itself is excluded.
    """
    if target_user_id not in similarity_matrix.index:
        return []

    scores = similarity_matrix.loc[target_user_id].drop(labels=[target_user_id])
    top    = scores.sort_values(ascending=False).head(n)
    return [(uid, round(float(score), 4)) for uid, score in top.items()]
