from fastapi import APIRouter, UploadFile, File
from app.services.upload_service import save_video
from app.services.metadata_service import get_video_metadata

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

@router.get("/test")
def test_api():
    return {
        "message": "Video API is Working"
    }

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path, unique_filename = save_video(file)
    metadata = get_video_metadata(file_path)

    return{
    "message": "Video uploaded successfully",
    "filename": unique_filename,
    "metadata": metadata
}