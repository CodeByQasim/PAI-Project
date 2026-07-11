from fastapi import FastAPI
from app.api.videos import router as video_router

app = FastAPI(
    title="AI Video Editing Backend"
)

app.include_router(video_router)

@app.get("/")
def home():
    return {
        "message": "Backend is Running"
    }