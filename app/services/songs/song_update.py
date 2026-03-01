from app.db.chroma import songs_collection

def update_song(user_id: str, track_id: str, request):

    song_id = f"{user_id}:{track_id}"
    
    result = songs_collection.get(ids=[song_id])

    if not result["ids"]:
        raise ValueError("Song not found")

    metadata = result["metadatas"][0]

    if metadata["user_id"] != user_id:
        raise ValueError("Unauthorized to update this song")

    # Update listened state
    if request.listened is not None:
        metadata["listened"] = request.listened

    # Update rating
    if request.rating is not None:
        metadata["rating"] = request.rating

    # Update my_tags (replace strategy)
    if request.my_tags is not None:
        metadata["my_tags"] = ",".join(
            t.lower() for t in request.my_tags
        )

    songs_collection.update(
        ids=[song_id],
        metadatas=[metadata]
    )

    return {
        "message": "Song updated successfully",
        "song_id": track_id
    }
