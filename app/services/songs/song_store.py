from datetime import datetime
from app.db.chroma import songs_collection
import requests

ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"

def fetch_song_details(track_id: str):
    params = {
        "id": track_id,
        "entity": "song"
    }

    res = requests.get(ITUNES_LOOKUP_URL, params=params)
    res.raise_for_status()

    results = res.json().get("results", [])

    if not results:
        return None

    # First result is the track
    track = results[0]

    return {
        "track_id": str(track["trackId"]),
        "title": track["trackName"],
        "artist": track["artistName"],
        "album": track.get("collectionName"),
        "year": track.get("releaseDate", "")[:4],
        "image_url": track.get("artworkUrl100"),
        "preview_url": track.get("previewUrl"),
        "source": "itunes"
    }

def add_song_to_list(user_id: str, request):
    track_id = request.track_id
    song_id = f"{user_id}:{track_id}"

    existing = songs_collection.get(ids=[song_id])
    if existing["ids"]:
        return {
            "message": "Song already exists",
            "track_id": track_id
        }
    
    song = fetch_song_details(track_id)
    if not song:
        raise ValueError("Song not found via iTunes lookup")

    document = f"""
    {song['title']}
    Artist: {song['artist']}
    Album: {song['album']}
    """

    metadata = {
        #OWNERSHIP
        "user_id": user_id,

        #SONG IDENTITY
        "track_id": track_id,
        "title": song['title'],
        "artist": song['artist'],
        "album": song['album'],
        "year": song['year'],
        "type": "song",
        "source": song['source'],

        # TAGS
        "friends_recommended": ",".join(t.lower() for t in request.friends_recommended) if request.friends_recommended else "",
        "my_tags": "",

        # STATE
        "listened": request.listened,
        "rating": request.rating,

        # MEDIA
        "image_url": song['image_url'],
        "preview_url": song['preview_url'],

        "created_at": datetime.utcnow().isoformat()
    }

    songs_collection.add(
        ids=[song_id],
        documents=[document.strip()],
        metadatas=[metadata]
    )

    return {
        "message": "Song added successfully",
        "track_id": track_id,
        "title": song['title']
    }
