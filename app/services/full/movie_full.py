import httpx
import os
from app.db.chroma import movies_collection

OMDB_KEY = os.getenv("OMDB_API_KEY") or "7b6d1d87"


def parse_csv_field(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


async def fetch_omdb(imdb_id: str):
    params = {
        "i": imdb_id,
        "apikey": OMDB_KEY,
        "plot": "full"
    }

    res = httpx.get("http://www.omdbapi.com/", params=params)
    res.raise_for_status()
    return res.json()


async def get_full_movie(imdb_id: str, user_id: str | None = None):

    # 1️⃣ Fetch provider data
    external = await fetch_omdb(imdb_id)

    user_entry = None

    # 2️⃣ Only check library if user exists
    if user_id:
        results = movies_collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"imdb_id": imdb_id}
                ]
            }
        )

        if results["metadatas"]:
            meta = results["metadatas"][0]

            user_entry = {
                "watched": meta.get("watched", False),
                "rating": meta.get("rating"),
                "friends_recommended": meta.get("friends_recommended"),
                "my_tags": meta.get("my_tags"),
            }

    # 3️⃣ Return unified structure
    return {
        "type": "movie",
        "id": external.get("imdbID"),

        "title": external.get("Title"),
        "subtitle": external.get("Rated"),
        "poster": external.get("Poster"),
        "genre": external.get("Genre"),
        "release_date": external.get("Released"),
        "description": external.get("Plot"),

        # full provider response
        "provider_data": external,

        # personalized layer
        "user_entry": user_entry,
    }