import os
import uuid
import shutil
from fastapi import UploadFile
from app.utils.validators import validate_video_file

UPLOAD_DIR = "app/uploads"


def save_video(file: UploadFile):
    validate_video_file(file.filename)

    # Agar uploads folder nahi hai to bana do
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # File ka complete path
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)   

    # File ko uploads folder me save karo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path, unique_filename