from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user, get_current_user_optional
from app.services.full.full_service import get_full_media
from app.schemas.full.full import FullMediaResponse

router = APIRouter(
    prefix="/full",
    tags=["Full Media"]
)

@router.get("/{media_type}/{media_id}", response_model=FullMediaResponse)
async def full_media(
    media_type: str,
    media_id: str,
    current_user: dict | None = Depends(get_current_user_optional)
):
    try:
        print("CURRENT USER IN FULL MEDIA:", current_user)
        return await get_full_media(media_type, media_id, current_user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
