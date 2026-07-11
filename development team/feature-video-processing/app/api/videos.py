from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import save_video
from app.services.metadata_service import get_video_metadata
import os
from pydantic import BaseModel
from app.services.ffmpeg_service import trim_video, merge_videos, burn_subtitles
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)
class TrimRequest(BaseModel):
    filename: str
    start_time: int
    end_time: int
class MergeRequest(BaseModel):
    filenames: list[str]
class SubtitleRequest(BaseModel):
    filename: str
    subtitle_file: str

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

@router.post("/trim")
def trim_video_api(request: TrimRequest):

    input_path = os.path.join("app/uploads", request.filename)

    if not os.path.exists(input_path):
     raise HTTPException(
        status_code=404,
        detail="Video not found."
    )
    
    if request.start_time >= request.end_time:
     raise HTTPException(
        status_code=400,
        detail="start_time must be less than end_time."
    )

    if request.start_time < 0 or request.end_time < 0:
     raise HTTPException(
        status_code=400,
        detail="Time cannot be negative."
    )

    output_path = trim_video(
        input_path=input_path,
        start_time=request.start_time,
        end_time=request.end_time
    )

    return {
        "message": "Video trimmed successfully",
        "output": output_path
    }

@router.post("/merge")
def merge_video_api(request: MergeRequest):

    # Kam az kam 2 videos honi chahiye
    if len(request.filenames) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 videos are required."
        )

    video_paths = []

    for filename in request.filenames:

        path = os.path.join("app/uploads", filename)

        if not os.path.exists(path):
            raise HTTPException(
                status_code=404,
                detail=f"{filename} not found."
            )

        video_paths.append(path)

    output = merge_videos(video_paths)

    return {
        "message": "Videos merged successfully",
        "output": output
    }

@router.post("/burn-subtitles")
def burn_subtitles_api(request: SubtitleRequest):

    video_path = os.path.join("app/uploads", request.filename)

    subtitle_path = os.path.join("app/subtitles", request.subtitle_file)

    if not os.path.exists(video_path):
        raise HTTPException(
            status_code=404,
            detail="Video not found."
        )

    if not os.path.exists(subtitle_path):
        raise HTTPException(
            status_code=404,
            detail="Subtitle file not found."
        )

    try:
     output = burn_subtitles(
        video_path=video_path,
        subtitle_path=subtitle_path
    )

     return {
        "message": "Subtitles burned successfully",
        "output": output
    }

    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/download/{filename}")
def download_video(filename: str):

    file_path = os.path.join("app/outputs", filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )