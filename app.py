from flask import Flask, render_template, request, jsonify, send_from_directory
from src.recommender import get_recommendations, get_all_movies
from src.utils import validate_ratings
import os, threading, time, urllib.request

app = Flask(__name__)

# ── Poster URLs (TMDB) ───────────────────────────────────────────
POSTER_URLS = {
    1:  "https://image.tmdb.org/t/p/w342/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    2:  "https://image.tmdb.org/t/p/w342/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    4:  "https://image.tmdb.org/t/p/w342/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    5:  "https://image.tmdb.org/t/p/w342/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    7:  "https://image.tmdb.org/t/p/w342/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
    9:  "https://image.tmdb.org/t/p/w342/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    10: "https://image.tmdb.org/t/p/w342/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    12: "https://image.tmdb.org/t/p/w342/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
    13: "https://image.tmdb.org/t/p/w342/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
    14: "https://image.tmdb.org/t/p/w342/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
    16: "https://image.tmdb.org/t/p/w342/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg",
    18: "https://image.tmdb.org/t/p/w342/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
    19: "https://image.tmdb.org/t/p/w342/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
    20: "https://image.tmdb.org/t/p/w342/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
}

def download_missing_posters():
    """Download any missing poster images in the background on startup."""
    poster_dir = os.path.join(os.path.dirname(__file__), "static", "posters")
    os.makedirs(poster_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for mid, url in POSTER_URLS.items():
        path = os.path.join(poster_dir, f"{mid}.jpg")
        if os.path.exists(path) and os.path.getsize(path) > 20_000:
            continue  # already have it
        try:
            req  = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) > 5_000:
                with open(path, "wb") as f:
                    f.write(data)
                print(f"  ✅ Downloaded poster {mid}")
        except Exception as e:
            print(f"  ⚠️  Could not download poster {mid}: {e}")
        time.sleep(0.3)
    print("  🎬 Poster check complete.")

# Download missing posters in background thread so server starts instantly
threading.Thread(target=download_missing_posters, daemon=True).start()


# ── Routes ───────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/movies", methods=["GET"])
def movies():
    try:
        return jsonify({"success": True, "movies": get_all_movies()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/recommend", methods=["POST"])
def recommend():
    try:
        data         = request.get_json()
        raw_ratings  = data.get("ratings", {})
        user_ratings = {int(k): float(v) for k, v in raw_ratings.items()}
        valid, error = validate_ratings(user_ratings)
        if not valid:
            return jsonify({"success": False, "error": error}), 400
        results = get_recommendations(user_ratings, top_k=6)
        return jsonify({"success": True, "recommendations": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("\n  🎬 CineMatch starting up…")
    print("  📥 Downloading any missing posters in the background…\n")
    app.run(debug=True)
