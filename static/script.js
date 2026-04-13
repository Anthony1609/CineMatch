/* ══════════════════════════════════════════
   CineMatch · script.js · v2.0
══════════════════════════════════════════ */

// Posters are stored locally in static/posters/ after running download_posters.py
const POSTERS = {};
for (let i = 1; i <= 20; i++) {
  POSTERS[i] = `/static/posters/${i}.jpg`;
}

const GENRE_CLASS = {
  "Sci-Fi":"g-SciFi", "Action":"g-Action", "Drama":"g-Drama",
  "Crime":"g-Crime",  "Thriller":"g-Thriller","Horror":"g-Horror",
  "War":"g-War",      "Romance":"g-Romance","Comedy":"g-Comedy"
};

/* ── State ──────────────────── */
let allMovies   = [];
let userRatings = {};
let userName    = "";

/* ── Navigation ─────────────── */
function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById("screen-" + id).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function navTo(id) {
  showScreen(id);
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  if (id === "intro")     document.getElementById("nav-home").classList.add("active");
  if (id === "developer") document.getElementById("nav-dev").classList.add("active");
}

/* ── Start ──────────────────── */
async function startApp() {
  const val = document.getElementById("name-input").value.trim();
  if (!val) { document.getElementById("name-input").focus(); return; }
  userName = val;
  document.getElementById("rate-username-display").textContent = userName;
  document.getElementById("result-username").textContent       = userName;
  await loadMovies();
  showScreen("rate");
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
}

document.getElementById("name-input").addEventListener("keydown", e => {
  if (e.key === "Enter") startApp();
});

/* ── Load movies from API ────── */
async function loadMovies() {
  const res  = await fetch("/api/movies");
  const data = await res.json();
  if (!data.success) { alert("Could not load movies."); return; }
  allMovies = data.movies;
  userRatings = {};
  renderGrid();
  updateProgress();
}

/* ── Render movie cards ─────── */
function renderGrid() {
  const grid = document.getElementById("movies-grid");
  grid.innerHTML = "";

  allMovies.forEach(movie => {
    const id     = movie.movie_id;
    const rated  = userRatings[id] || 0;
    const poster = POSTERS[id] || "";
    const gc     = GENRE_CLASS[movie.genre] || "";

    const card = document.createElement("div");
    card.className = "movie-card" + (rated > 0 ? " rated" : "");
    card.id = "card-" + id;
    card.innerHTML = `
      <div class="card-img-wrap">
        <img class="card-poster" src="${poster}" alt="${movie.title}" loading="lazy"
          onerror="this.style.background='#111e33';this.style.height='200px'"/>
      </div>
      <div class="card-body">
        <div class="card-title">${movie.title}</div>
        <div class="card-meta">
          <span class="genre-badge ${gc}">${movie.genre}</span>
          <span class="card-year">${movie.year}</span>
        </div>
        <div class="star-row" id="stars-${id}"></div>
      </div>
    `;
    grid.appendChild(card);
    renderStars(id, rated);
  });
}

/* ── Stars ──────────────────── */
function renderStars(movieId, current) {
  const row = document.getElementById("stars-" + movieId);
  if (!row) return;
  row.innerHTML = "";
  for (let s = 1; s <= 5; s++) {
    const star = document.createElement("span");
    star.className = "star" + (s <= current ? " lit" : "");
    star.textContent = "★";
    star.addEventListener("mouseenter", () => hlStars(movieId, s));
    star.addEventListener("mouseleave", () => hlStars(movieId, userRatings[movieId] || 0));
    star.addEventListener("click",      () => setRating(movieId, s));
    row.appendChild(star);
  }
}

function hlStars(id, n) {
  const row = document.getElementById("stars-" + id);
  if (!row) return;
  row.querySelectorAll(".star").forEach((s, i) => s.classList.toggle("lit", i < n));
}

function setRating(id, val) {
  if (userRatings[id] === val) { delete userRatings[id]; val = 0; }
  else { userRatings[id] = val; }

  renderStars(id, val);
  const card = document.getElementById("card-" + id);
  if (card) card.classList.toggle("rated", val > 0);

  updateProgress();
  updateSidebar();
}

/* ── Progress ───────────────── */
function updateProgress() {
  const count = Object.keys(userRatings).length;
  const total = allMovies.length;
  const pct   = (count / total) * 100;
  const circ  = 169.6;

  // circular ring
  const circle = document.getElementById("prog-circle");
  if (circle) circle.style.strokeDashoffset = circ - (circ * count / total);
  const txt = document.getElementById("prog-text");
  if (txt) txt.textContent = count;

  const lbl = document.getElementById("progress-label");
  if (lbl) lbl.textContent = count + " / 20 rated";

  const btn = document.getElementById("btn-recommend");
  if (btn) {
    btn.disabled   = count < 3;
    btn.textContent = count < 3 ? `Rate ${3 - count} more` : "Get Picks →";
  }
}

/* ── Sidebar ────────────────── */
function updateSidebar() {
  const list    = document.getElementById("sidebar-list");
  const empty   = document.getElementById("sidebar-empty");
  const cta     = document.getElementById("sidebar-cta");
  const countEl = document.getElementById("sidebar-count");

  const rated = Object.entries(userRatings);
  countEl.textContent = rated.length;

  if (rated.length === 0) {
    empty.style.display = "block";
    list.style.display  = "none";
    cta.style.display   = "none";
    return;
  }

  empty.style.display = "none";
  list.style.display  = "flex";
  cta.style.display   = rated.length >= 3 ? "block" : "none";

  list.innerHTML = "";
  rated.forEach(([id, rating]) => {
    const movie  = allMovies.find(m => m.movie_id === Number(id));
    if (!movie) return;
    const stars  = "★".repeat(rating) + "☆".repeat(5 - rating);
    const poster = POSTERS[id] || "";

    const item = document.createElement("div");
    item.className = "sb-item";
    item.id = "sb-" + id;
    item.innerHTML = `
      <img class="sb-poster" src="${poster}" alt="${movie.title}" loading="lazy"
        onerror="this.style.background='#162440';this.style.minWidth='36px'"/>
      <div class="sb-info">
        <div class="sb-title">${movie.title}</div>
        <div class="sb-stars">${stars}</div>
      </div>
      <button class="sb-remove" onclick="removeRating(${id})" title="Remove">✕</button>
    `;
    list.appendChild(item);
  });
}

function removeRating(id) {
  delete userRatings[id];
  renderStars(id, 0);
  const card = document.getElementById("card-" + id);
  if (card) card.classList.remove("rated");
  updateProgress();
  updateSidebar();
}

/* ── Submit to Flask API ─────── */
async function submitRatings() {
  if (Object.keys(userRatings).length < 3) return;

  showScreen("results");

  const vals = Object.values(userRatings);
  const avg  = (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1);
  document.getElementById("rs-rated").textContent = vals.length;
  document.getElementById("rs-avg").textContent   = avg;

  document.getElementById("loading-indicator").style.display = "block";
  document.getElementById("results-content").style.display   = "none";

  try {
    const res  = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ratings: userRatings })
    });
    const data = await res.json();
    document.getElementById("loading-indicator").style.display = "none";

    if (!data.success) { alert("Error: " + data.error); return; }

    document.getElementById("rs-recs").textContent = data.recommendations.length;
    renderRecs(data.recommendations);
    renderRatedResults();
    document.getElementById("results-content").style.display = "block";
  } catch (err) {
    document.getElementById("loading-indicator").style.display = "none";
    alert("Network error: " + err.message);
  }
}

/* ── Render recs ─────────────── */
function renderRecs(recs) {
  const grid = document.getElementById("recs-grid");
  grid.innerHTML = "";
  recs.forEach((rec, i) => {
    const poster = POSTERS[rec.movie_id] || "";
    const gc     = GENRE_CLASS[rec.genre] || "";
    const stars  = "★".repeat(Math.round(rec.predicted_rating)) +
                   "☆".repeat(5 - Math.round(rec.predicted_rating));

    const card = document.createElement("div");
    card.className = "rec-card";
    card.innerHTML = `
      <div class="rec-poster-wrap">
        <img class="rec-poster" src="${poster}" alt="${rec.title}" loading="lazy"
          onerror="this.style.background='#111e33'"/>
        <div class="rec-rank">#${i + 1} Pick</div>
        <div class="rec-overlay">
          <div class="rec-overlay-content">
            <div class="rec-title-overlay">${rec.title}</div>
            <div class="rec-meta-overlay">
              <span class="genre-badge ${gc}">${rec.genre}</span>
              <span class="rec-year">${rec.year}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="rec-body">
        <div class="rec-stars">${stars}</div>
        <div class="rec-pred">Predicted rating: <span>${rec.predicted_rating} / 5</span></div>
        <div class="match-row">
          <span>Match Score</span>
          <span class="match-val">${rec.match_pct}%</span>
        </div>
        <div class="match-bar">
          <div class="match-fill" style="width:0%" data-w="${rec.match_pct}"></div>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });

  setTimeout(() => {
    document.querySelectorAll(".match-fill").forEach(el => {
      el.style.width = el.dataset.w + "%";
    });
  }, 120);
}

/* ── Render rated films on results ── */
function renderRatedResults() {
  const grid = document.getElementById("rated-list-results");
  grid.innerHTML = "";
  Object.entries(userRatings).forEach(([id, rating]) => {
    const movie  = allMovies.find(m => m.movie_id === Number(id));
    if (!movie) return;
    const poster = POSTERS[id] || "";
    const stars  = "★".repeat(rating) + "☆".repeat(5 - rating);
    const card   = document.createElement("div");
    card.className = "rr-card";
    card.innerHTML = `
      <img class="rr-poster" src="${poster}" alt="${movie.title}" loading="lazy"
        onerror="this.style.background='#111e33';this.style.height='100px'"/>
      <div class="rr-info">
        <div class="rr-title">${movie.title}</div>
        <div class="rr-stars">${stars}</div>
      </div>
    `;
    grid.appendChild(card);
  });
}

/* ── Reset helpers ───────────── */
function rateAgain()  { userRatings = {}; renderGrid(); updateProgress(); updateSidebar(); showScreen("rate"); }
function startOver()  { userRatings = {}; userName = ""; document.getElementById("name-input").value = ""; showScreen("intro"); document.getElementById("nav-home").classList.add("active"); }
