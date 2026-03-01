import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(
        persist_directory="/app/chroma",
        anonymized_telemetry=False
    )
)

movies_collection = client.get_or_create_collection(
    name="movies"
)

songs_collection = client.get_or_create_collection(
    name="songs"
)
