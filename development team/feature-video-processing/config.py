import os
from dotenv import load_dotenv

load_dotenv()

FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")