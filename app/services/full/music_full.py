import httpx
from app.db.chroma import songs_collection

async def fetch_itunes(track_id: str):
    url = "https://itunes.apple.com/lookup"
    params = {"id": track_id}

    res = httpx.get(url, params=params)
    res.raise_for_status()

    data = res.json()
    return data["results"][0] if data["resultCount"] > 0 else None


async def get_full_music(track_id: str, user_id: str | None = None):

    # 1️⃣ Fetch provider data
    external = await fetch_itunes(track_id)

    if not external:
        raise ValueError("Track not found")

    user_entry = None

    # 2️⃣ Fetch user-specific metadata
    if user_id:
        results = songs_collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"track_id": track_id}
                ]
            }
        )

        if results["metadatas"]:
            meta = results["metadatas"][0]

            user_entry = {
                "listened": meta.get("listened", False),
                "rating": meta.get("rating"),
                "friends_recommended": meta.get("friends_recommended"),
                "my_tags": meta.get("my_tags"),
            }

    # 3️⃣ Unified return shape
    return {
        "type": "music",
        "id": str(external.get("trackId")),

        "title": external.get("trackName"),
        "subtitle": external.get("artistName"),
        "poster": external.get("artworkUrl100"),
        "genre": external.get("primaryGenreName"),
        "release_date": external.get("releaseDate"),
        "description": None,  # music doesn’t have plot

        "provider_data": external,

        "user_entry": user_entry,
    }