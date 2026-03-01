import os
import requests
from datetime import datetime
from ...db.chroma import movies_collection

OMDB_API_KEY = os.getenv("OMDB_API_KEY") or "7b6d1d87"
OMDB_URL = "https://www.omdbapi.com/"

def fetch_movie_details(imdb_id: str):
    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    res = requests.get(OMDB_URL, params=params)
    res.raise_for_status()

    data = res.json()
    if data.get("Response") == "False":
        raise ValueError(data.get("Error"))

    return data

def add_movie_to_watchlist(user_id: str, request):
    imdb_id = request.imdb_id
    movie_id = f"{user_id}:{imdb_id}"
    # 🔒 Deduplication check
    existing = movies_collection.get(
        ids=[movie_id],
    )

    if existing["ids"]:
        return {
            "message": "Movie already exists in watchlist",
            "imdb_id": imdb_id
        }

    movie = fetch_movie_details(imdb_id)

    document = f"""
    {movie['Title']} ({movie.get('Year')})
    Director: {movie.get('Director')}
    Genre: {movie.get('Genre')}
    Plot: {movie.get('Plot')}
    """

    friends_recommended_str = ",".join(t.lower() for t in request.friends_recommended)
    friends_recommended_str = friends_recommended_str or ""

    metadata = {
        "user_id": user_id,
        "imdb_id": imdb_id,
        "title": movie["Title"],
        "year": movie.get("Year"),
        "genre": movie.get("Genre"),
        "director": movie.get("Director"),
        "type": "movie",
        "friends_recommended": friends_recommended_str,
        "my_tags": "",
        "watched": request.watched,
        "rating": request.rating,
        "image_url": movie.get("Poster") if movie.get("Poster") != "N/A" else None,
        "created_at": datetime.utcnow().isoformat()
    }

    metadata = {k: v for k, v in metadata.items() if v is not None}

    movies_collection.add(
        ids=[movie_id],
        documents=[document.strip()],
        metadatas=[metadata]
    )

    return {
        "message": "Movie added successfully",
        "imdb_id": imdb_id,
        "title": movie["Title"]
    }