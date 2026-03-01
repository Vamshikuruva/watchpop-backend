from app.services.full.movie_full import get_full_movie
from app.services.full.music_full import get_full_music

async def get_full_media(media_type: str, media_id: str, user: dict | None = None):

    if media_type == "movie":
        return await get_full_movie(
            imdb_id=media_id,
            user_id=user["id"] if user else None
        )

    elif media_type == "music":
        return await get_full_music(
            track_id = media_id,
            user_id=user["id"] if user else None
        )

    else:
        raise Exception("Invalid media type")
