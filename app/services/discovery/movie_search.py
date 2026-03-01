import os
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY") or "7b6d1d87"
OMDB_BASE_URL = "http://www.omdbapi.com/"

def search_movie(query: str):
    params = {
        "apikey": OMDB_API_KEY,
        "s": query,
        "type": "movie"
    }

    response = requests.get(OMDB_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if data.get("Response") == "False":
        return []
    
    results = []
    for item in data.get("Search", []):
        movie = {
            "external_id": item["imdbID"],
            "title": item["Title"],
            "year": item["Year"],
            "image_url": item["Poster"] if item["Poster"] != "N/A" else None,
            "source": "omdb"
        }
        results.append(movie)
    
    return results