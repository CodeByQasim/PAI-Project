import cv2
import os

def get_video_metadata(video_path: str):

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        return None

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    duration = frame_count / fps if fps > 0 else 0

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    file_size = round(os.path.getsize(video_path) / (1024 * 1024), 2)

    video.release()

    return {
        "duration_seconds": round(duration, 2),
        "fps": round(fps, 2),
        "resolution": f"{width}x{height}",
        "file_size_mb": file_size
    }