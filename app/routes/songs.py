from fastapi import APIRouter, Depends, Query, HTTPException
from app.auth.dependencies import get_current_user
from app.schemas.songs.song import SongAddRequest
from app.schemas.songs.song_update import SongUpdateRequest
from app.services.songs.song_query import list_songs
from app.services.songs.song_update import update_song
from app.services.songs.song_store import add_song_to_list

router = APIRouter(
    prefix="/songs", 
    tags=["Songs"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def add_song(song: SongAddRequest, user = Depends(get_current_user)):
    return add_song_to_list(user["id"], song)

@router.get("/")
def get_songs(
    user = Depends(get_current_user),
    listened: bool | None = Query(None),
    friends_recommended: str | None = Query(None),
    my_tags: str | None = Query(None),
    sort_by: str | None = Query(
        None,
        pattern="^(title|artist|year|rating|created_at|listened)$"
    ),
    order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    ),
    limit: int = Query(20, ge=1, le=100)
):
    return list_songs(
        user_id=user["id"],
        listened=listened,
        friends_recommended=friends_recommended,
        my_tags=my_tags,
        sort_by=sort_by,
        order=order,
        limit=limit
    )

@router.patch("/{track_id}")
def update_song_api(track_id: str, request: SongUpdateRequest, user = Depends(get_current_user)):
    try:
        return update_song(user["id"], track_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))