def format_stars(rating: float) -> str:
    """Convert a numeric rating (1-5) into a star string."""
    filled = int(round(rating))
    empty  = 5 - filled
    return "★" * filled + "☆" * empty


def validate_ratings(user_ratings: dict) -> tuple[bool, str]:
    """
    Validate that user-submitted ratings are well-formed.
    Returns (is_valid: bool, error_message: str).
    """
    if not isinstance(user_ratings, dict):
        return False, "Ratings must be a dictionary."
    if len(user_ratings) < 3:
        return False, "Please rate at least 3 movies before getting recommendations."
    for mid, rating in user_ratings.items():
        if not isinstance(rating, (int, float)):
            return False, f"Rating for movie {mid} must be a number."
        if not (1 <= rating <= 5):
            return False, f"Rating for movie {mid} must be between 1 and 5."
    return True, ""
