import requests

ITUNES_URL = "https://itunes.apple.com/search"

def search_song(query: str):
    params = {
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": 10
    }

    res = requests.get(ITUNES_URL, params=params)
    res.raise_for_status()

    results = []
    for item in res.json().get("results", []):
        results.append({
            "external_id": str(item["trackId"]),
            "title": item["trackName"],
            "artist": item["artistName"],
            "album": item.get("collectionName"),
            "year": item.get("releaseDate", "")[:4],
            "image_url": item.get("artworkUrl100"),
            "preview_url": item.get("previewUrl"),
            "source": "itunes"
        })

    return results
