"""
download_posters.py
-------------------
Run this ONCE to download all 20 real movie poster images.
Saves them to static/posters/ — served locally forever after.

Usage:
    python download_posters.py
"""

import os, time, urllib.request

# Multiple fallback URLs per movie — tries each until one works
POSTERS = {
    1:  ["https://image.tmdb.org/t/p/w342/qJ2tW6WMUDux911r6m7haRef0WH.jpg"],
    2:  ["https://image.tmdb.org/t/p/w342/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"],
    3:  ["https://image.tmdb.org/t/p/w342/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"],
    4:  ["https://image.tmdb.org/t/p/w342/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"],
    5:  ["https://image.tmdb.org/t/p/w342/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"],
    6:  ["https://image.tmdb.org/t/p/w342/lyQBXzOQSuE59IsHyhrp0qIiPAz.jpg"],
    7:  ["https://image.tmdb.org/t/p/w342/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"],
    8:  [                                                                         # The Godfather
        "https://image.tmdb.org/t/p/w342/rSPw7tgCH9c6NqICZef4kZjFOQ5.jpg",
        "https://image.tmdb.org/t/p/w342/eEslKSwcqmiNS6va24Pbxf2UKmJ.jpg",
        "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
    ],
    9:  ["https://image.tmdb.org/t/p/w342/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"],
    10: ["https://image.tmdb.org/t/p/w342/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"],
    11: ["https://image.tmdb.org/t/p/w342/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg"],
    12: ["https://image.tmdb.org/t/p/w342/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg"],
    13: ["https://image.tmdb.org/t/p/w342/or06FN3Dka5tukK1e9sl16pB3iy.jpg"],
    14: ["https://image.tmdb.org/t/p/w342/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"],
    15: [                                                                         # 1917
        "https://image.tmdb.org/t/p/w342/uZO5pkHZC3rznvdD3Iq6YbgkXAc.jpg",
        "https://image.tmdb.org/t/p/w342/U7QOzDJiAVxqplJQPAkLxCDWYiY.jpg",
        "https://upload.wikimedia.org/wikipedia/en/9/95/1917_Film_poster.jpg",
    ],
    16: ["https://image.tmdb.org/t/p/w342/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"],
    17: [                                                                         # Mad Max Fury Road
        "https://image.tmdb.org/t/p/w342/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg",
        "https://image.tmdb.org/t/p/w342/hA2ple9q4qnwxp3hKVNhroipsir.jpg",
        "https://upload.wikimedia.org/wikipedia/en/6/6e/Mad_Max_Fury_Road.jpg",
    ],
    18: ["https://image.tmdb.org/t/p/w342/7fn624j5lj3xTme2SgiLCeuedmO.jpg"],
    19: ["https://image.tmdb.org/t/p/w342/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"],
    20: ["https://image.tmdb.org/t/p/w342/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"],
}

NAMES = {
    1:"The Dark Knight", 2:"Inception", 3:"The Matrix", 4:"Interstellar",
    5:"Parasite", 6:"The Shawshank Redemption", 7:"Pulp Fiction", 8:"The Godfather",
    9:"Fight Club", 10:"Forrest Gump", 11:"The Silence of the Lambs", 12:"Goodfellas",
    13:"Avengers: Endgame", 14:"Joker", 15:"1917", 16:"Get Out",
    17:"Mad Max: Fury Road", 18:"Whiplash", 19:"La La Land", 20:"Blade Runner 2049",
}

# These were manually uploaded as real posters — never overwrite them
KEEP = {3, 6, 11}

def download(url, headers, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return data if len(data) > 5_000 else None

def main():
    base   = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(base, "static", "posters")
    os.makedirs(outdir, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    ok, failed = [], []

    print("=" * 55)
    print("  CineMatch — Movie Poster Downloader")
    print("=" * 55)
    print()

    for mid, urls in POSTERS.items():
        path = os.path.join(outdir, f"{mid}.jpg")

        # Keep manually uploaded real posters
        if mid in KEEP and os.path.exists(path):
            print(f"  ✓  {mid:>2}. {NAMES[mid]}  (real poster — keeping)")
            ok.append(mid)
            continue

        # Skip already-downloaded posters (not in KEEP)
        if mid not in KEEP and os.path.exists(path) and os.path.getsize(path) > 20_000:
            print(f"  ✓  {mid:>2}. {NAMES[mid]}  (already downloaded)")
            ok.append(mid)
            continue

        # Try each URL until one works
        downloaded = False
        for url in urls:
            try:
                data = download(url, headers)
                if data:
                    with open(path, "wb") as f:
                        f.write(data)
                    print(f"  ✅  {mid:>2}. {NAMES[mid]}  ({len(data)//1024} KB)")
                    ok.append(mid)
                    downloaded = True
                    break
            except Exception:
                continue

        if not downloaded:
            print(f"  ❌  {mid:>2}. {NAMES[mid]}  (all URLs failed)")
            failed.append(mid)

        time.sleep(0.25)

    print()
    print("=" * 55)
    print(f"  Done!  {len(ok)}/20 posters ready,  {len(failed)} failed")
    if failed:
        print(f"  Failed: {[NAMES[i] for i in failed]}")
        print()
        print("  For failed movies, manually save a poster image as:")
        for i in failed:
            print(f"    static/posters/{i}.jpg   ({NAMES[i]})")
    else:
        print("  All 20 real posters ready!")
        print("  Now run:  python app.py")
    print("=" * 55)

if __name__ == "__main__":
    main()
