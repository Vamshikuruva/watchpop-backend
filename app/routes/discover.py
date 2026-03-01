from fastapi import APIRouter, Query
from app.services.discovery.movie_search import search_movie
from app.services.discovery.song_search import search_song

router = APIRouter(
    prefix="/discover",
    tags=["Discover"]
)

@router.get("/movies")
def discover_movies(query: str = Query(..., min_length=2)):
    return search_movie(query)

@router.get("/songs")
def discover_songs(query: str = Query(..., min_length=2)):
    return search_song(query)