# CineMatch — Simple Recommendation System
## CSC 309 Mini Project 4

A Python web app that recommends movies using **Collaborative Filtering**
built with **Flask**, **Pandas**, and **NumPy**.

---

## Project Structure

```
recommendation_system/
├── data/
│   ├── ratings.csv        ← User-item ratings dataset
│   └── movies.csv         ← Movie catalogue
├── src/
│   ├── __init__.py
│   ├── data_loader.py     ← Loads CSVs, builds User-Item Matrix (Pandas)
│   ├── similarity.py      ← Cosine similarity computation (NumPy)
│   ├── recommender.py     ← Core recommendation engine
│   └── utils.py           ← Validation helpers
├── templates/
│   └── index.html         ← Frontend HTML (3 screens)
├── static/
│   ├── style.css          ← Dark cinematic styling
│   └── script.js          ← Frontend logic (fetch API calls)
├── app.py                 ← Flask entry point
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Open the folder in VSCode
```
File → Open Folder → recommendation_system
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## How It Works

1. **User rates movies** via the web UI (star ratings 1–5)
2. `app.py` receives ratings via `POST /api/recommend`
3. `data_loader.py` loads `ratings.csv` and builds a **User-Item Matrix** using `pandas.pivot_table()`
4. The new user's ratings are appended as a temporary row
5. `similarity.py` computes **cosine similarity** (NumPy dot product) between the new user and all existing users
6. `recommender.py` finds top-3 most similar neighbours and performs a **weighted average prediction** for all unrated movies
7. Top 6 recommendations are returned as JSON and rendered in the browser

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Renders the web app |
| GET | `/api/movies` | Returns all 20 movies as JSON |
| POST | `/api/recommend` | Accepts ratings, returns recommendations |

### POST `/api/recommend` — Example Request
```json
{
  "ratings": {
    "1": 5,
    "3": 4,
    "9": 5
  }
}
```

### Response
```json
{
  "success": true,
  "recommendations": [
    {
      "movie_id": 2,
      "title": "Inception",
      "genre": "Sci-Fi",
      "year": 2010,
      "predicted_rating": 4.67,
      "match_pct": 93
    }
  ]
}
```
