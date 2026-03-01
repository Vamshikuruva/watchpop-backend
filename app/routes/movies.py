from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.dependencies import get_current_user
from app.schemas.movies.movie import MovieAddRequest
from app.services.movies.movie_store import add_movie_to_watchlist
from app.services.movies.movie_query import list_movies
from app.schemas.movies.movie_update import MovieUpdateRequest
from app.services.movies.movie_update import update_movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def add_movie(movie: MovieAddRequest, user=Depends(get_current_user)):
    return add_movie_to_watchlist(user["id"], movie)

@router.get("/")
def get_movies(
    user = Depends(get_current_user),
    watched: bool | None = Query(None),
    friends_recommended: str | None = Query(None),
    my_tag: str | None = Query(None),
    sort_by: str | None = Query(
        None,
        pattern="^(title|year|rating|created_at|watched)$"
    ),
    order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    ),
    limit: int = Query(20, ge=1, le=100)
):
    return list_movies(
        user_id=user["id"],
        watched=watched,
        friends_recommended=friends_recommended,
        my_tag=my_tag,
        sort_by=sort_by,
        order=order,
        limit=limit
    )

@router.patch("/{imdb_id}")
def update_movie_api(imdb_id: str, payload: MovieUpdateRequest, user = Depends(get_current_user)):
    try:
        return update_movie(user["id"], imdb_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))