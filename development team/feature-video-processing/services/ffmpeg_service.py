import os
import uuid
import subprocess


OUTPUT_DIR = "app/outputs"


def trim_video(input_path: str, start_time: int, end_time: int):

    # Output folder create karo agar nahi hai
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Unique output filename
    output_filename = f"trimmed_{uuid.uuid4()}.mp4"

    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Duration calculate
    duration = end_time - start_time

    command = [
        "ffmpeg",
        "-i", input_path,
        "-ss", str(start_time),
        "-t", str(duration),
        "-c", "copy",
        output_path,
        "-y"
    ]

    try:
     subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )

    except subprocess.CalledProcessError as e:
     raise Exception(f"FFmpeg Error: {e.stderr}")

    return output_path

def merge_videos(video_paths: list):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_filename = f"merged_{uuid.uuid4()}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Temporary file list
    list_file = os.path.join(OUTPUT_DIR, "videos.txt")

    with open(list_file, "w") as f:
        for video in video_paths:
            f.write(f"file '{os.path.abspath(video)}'\n")

    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file,
        "-c",
        "copy",
        output_path,
        "-y"
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg Error: {e.stderr}")

    return output_path

def burn_subtitles(video_path: str, subtitle_path: str):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_filename = f"subtitled_{uuid.uuid4()}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Windows path ko FFmpeg ke liye theek banao
    subtitle_path = os.path.abspath(subtitle_path)
    subtitle_path = subtitle_path.replace("\\", "/")
    subtitle_path = subtitle_path.replace(":", "\\:")

    print("Video:", video_path)
    print("Subtitle:", subtitle_path)

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{subtitle_path}'",
        "-c:a", "copy",
        output_path,
        "-y"
    ]

    print(command)

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg Error:\n{e.stderr}")

    return output_path