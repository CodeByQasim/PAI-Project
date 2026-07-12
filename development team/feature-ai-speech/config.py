import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env — check your .env file")

# Optional, with sensible defaults so nothing breaks if not set in .env
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
TRANSCRIPTS_DIR = os.getenv("TRANSCRIPTS_DIR", "transcripts")