from fastapi import HTTPException

# Allowed video extensions
ALLOWED_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]

def validate_video_file(filename: str):
    """
    Check if uploaded file is a valid video.
    """

    filename = filename.lower()

    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only MP4, MOV, AVI and MKV files are allowed."
        )

    return True