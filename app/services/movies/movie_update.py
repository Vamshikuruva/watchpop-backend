from app.db.chroma import movies_collection

def update_movie(user_id: str, imdb_id: str, request):
    movie_id = f"{user_id}:{imdb_id}"
    result = movies_collection.get(
        ids=[movie_id]
    )

    if not result["ids"]:
        raise ValueError("Movie not found")

    metadata = result["metadatas"][0]

    if metadata.get("user_id") != user_id:
        raise ValueError("Unauthorized")

    # Update watched
    if request.watched is not None:
        metadata["watched"] = request.watched

    # Update rating
    if request.rating is not None:
        metadata["rating"] = request.rating

    # Update my_tags (replace strategy)
    if request.my_tags is not None:
        metadata["my_tags"] = request.my_tags

    movies_collection.update(
        ids=[movie_id],
        metadatas=[metadata]
    )

    return {
        "message": "Movie updated successfully",
        "imdb_id": imdb_id
    }
