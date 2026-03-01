from app.db.chroma import movies_collection


def recommended_by(friend: str, metadata: dict) -> bool:
    if not metadata or not metadata.get("friends_recommended"):
        return False

    friends = [
        f.strip().lower()
        for f in metadata["friends_recommended"].split(",")
    ]

    return friend.lower() in friends


def metadata_contains(value: str, metadata_value: str) -> bool:
    if not metadata_value:
        return False

    items = [
        v.strip().lower()
        for v in metadata_value.split(",")
    ]

    return value.lower() in items


def list_movies(
    user_id: str,
    watched: bool | None = None,
    friends_recommended: str | None = None,
    my_tag: str | None = None,
    sort_by: str | None = None,
    order: str = "asc",
    limit: int = 20
):
    conditions = [{"user_id": user_id}]

    if watched is not None:
        conditions.append({"watched": watched})

    if len(conditions) == 1:
        where = conditions[0]
    else:
        where = {"$and": conditions}

    results = movies_collection.get(
        where=where if where else None,
    )

    # ✅ ALWAYS initialize these
    ids = results["ids"]
    metadatas = results["metadatas"]

    # 🔍 FRIEND FILTER
    if friends_recommended:
        query_friends = [
            f.strip().lower()
            for f in friends_recommended.split(",")
        ]

        filtered = [
            (ids[i], metadatas[i])
            for i in range(len(ids))
            if any(
                recommended_by(friend, metadatas[i])
                for friend in query_friends
            )
        ]

        ids, metadatas = zip(*filtered) if filtered else ([], [])

    # 🔍 TAG FILTER
    if my_tag:
        query_tags = [
            t.strip().lower()
            for t in my_tag.split(",")
        ]

        filtered = [
            (ids[i], metadatas[i])
            for i in range(len(ids))
            if any(
                metadata_contains(tag, metadatas[i].get("my_tags", ""))
                for tag in query_tags
            )
        ]

        ids, metadatas = zip(*filtered) if filtered else ([], [])

    # 🧱 Build response USING FILTERED DATA
    movies = []
    for movie_id, meta in zip(ids, metadatas):
        movies.append({
            "imdb_id": meta.get("imdb_id"),
            "title": meta.get("title"),
            "year": meta.get("year"),
            "image_url": meta.get("image_url"),
            "watched": meta.get("watched"),
            "friends_recommended": meta.get("friends_recommended"),
            "my_tags": meta.get("my_tags"),
            "rating": meta.get("rating"),
        })

    # 🔽 SORTING (Python-side)
    if sort_by:
        reverse = order == "desc"
        movies.sort(
            key=lambda m: (m.get(sort_by) is None, m.get(sort_by)),
            reverse=reverse
        )

    return movies
