from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.discover import router as discover_router
from app.routes.movies import router as movies_router
from app.routes.songs import router as songs_router
from app.routes.full import router as full_router

app = FastAPI(title="Movies & Songs Watchlist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://watchpop.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(auth_router)
app.include_router(discover_router)
app.include_router(movies_router)
app.include_router(songs_router)
app.include_router(full_router)
