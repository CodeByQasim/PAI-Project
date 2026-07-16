"""
Whisper speech-to-text integration for PAI-Project (Team 4 - AI & Speech Processing)

Day 1: base setup + transcribed sample.mp3 (done)
Day 2: test speech-to-text on one sample video, save transcript (done below)
Day 3: error handling for edge cases - missing file, unsupported format, empty audio (done below)
"""

import os
import json
from datetime import datetime, timezone
import whisper
from config import WHISPER_MODEL_SIZE, TRANSCRIPTS_DIR

# Load once at module level - loading per-call is slow and wastes memory
_model = None

SUPPORTED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".mov", ".mkv", ".avi", ".flac", ".ogg"}


class TranscriptionError(Exception):
    """Raised when transcription fails for a reason the caller should know about."""
    pass


def _get_model():
    global _model
    if _model is None:
        print(f"Loading Whisper '{WHISPER_MODEL_SIZE}' model (first run downloads it, then it's cached)...")
        _model = whisper.load_model(WHISPER_MODEL_SIZE)
    return _model

def _format_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format:
    HH:MM:SS,mmm
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def _format_vtt_timestamp(seconds: float) -> str:
    """
    Convert seconds to WebVTT timestamp format:
    HH:MM:SS.mmm
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02}.{milliseconds:03}"




def transcribe_audio(file_path: str) -> dict:
    """
    Transcribe an audio/video file with Whisper.
    Returns a dict with text, language, and segments.
    Raises TranscriptionError for missing files, bad formats, or empty audio.
    """
    if not os.path.exists(file_path):
        raise TranscriptionError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise TranscriptionError(
            f"Unsupported file format '{ext}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if os.path.getsize(file_path) == 0:
        raise TranscriptionError(f"File is empty (0 bytes): {file_path}")

    try:
        model = _get_model()
        result = model.transcribe(file_path)
    except Exception as e:
        # Common real-world cause: ffmpeg missing or file is corrupted/unreadable audio
        raise TranscriptionError(f"Whisper failed to transcribe '{file_path}': {e}")

    text = result.get("text", "").strip()
    if not text:
        raise TranscriptionError(f"Transcription produced no text - '{file_path}' may be silent or unreadable audio")

    return {
        "text": text,
        "language": result.get("language", "unknown"),
        "segments": result.get("segments", []),
    }


def generate_srt(transcript: dict) -> str:
    """
    Generate SRT subtitle content from a Whisper transcript.
    """
    segments = transcript.get("segments", [])

    if not segments:
        raise TranscriptionError("No transcript segments found to generate subtitles.")

    srt_lines = []

    for index, segment in enumerate(segments, start=1):
        start = _format_timestamp(segment["start"])
        end = _format_timestamp(segment["end"])
        text = segment["text"].strip()

        srt_lines.append(f"{index}")
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(text)
        srt_lines.append("")  # Blank line between subtitles

    return "\n".join(srt_lines)

def save_srt(source_file: str, srt_content: str, transcripts_dir: str = TRANSCRIPTS_DIR) -> str:
    """
    Save SRT subtitle content to disk and return the saved file path.
    """
    os.makedirs(transcripts_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(transcripts_dir, f"{base_name}_{timestamp}.srt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    return out_path

def save_vtt(source_file: str, transcript: dict, transcripts_dir: str = TRANSCRIPTS_DIR) -> str:
    """
    Save subtitle file in WebVTT (.vtt) format.
    """
    import os

    os.makedirs(transcripts_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(transcripts_dir, f"{base_name}_{timestamp}.vtt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")

        for segment in transcript["segments"]:
            start = _format_vtt_timestamp(segment["start"])
            end = _format_vtt_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    return out_path

def save_transcript(source_file: str, transcript: dict, transcripts_dir: str = TRANSCRIPTS_DIR) -> str:
    """
    Save a transcript to disk as JSON (full detail) and return the saved file path.
    Filename is based on the source file name + timestamp, so repeated runs don't overwrite each other.
    """
    os.makedirs(transcripts_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(transcripts_dir, f"{base_name}_{timestamp}.json")

    payload = {
        "source_file": source_file,
        "generated_at_utc": timestamp,
        "language": transcript["language"],
        "text": transcript["text"],
        "segments": transcript["segments"],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return out_path


if __name__ == "__main__":
    sample = "sample.mp3"
    try:
        print(f"Transcribing '{sample}'...")
        transcript = transcribe_audio(sample)
        print("Detected language:", transcript["language"])
        print("Transcript text:", transcript["text"])

        saved_path = save_transcript(sample, transcript)
        print(f"Transcript saved to: {saved_path}")
        # Generate SRT subtitles
        srt_content = generate_srt(transcript)

        srt_path = save_srt(sample, srt_content)

        print(f"SRT subtitle saved to: {srt_path}")

        print("\n----- SRT Preview -----")
        print(srt_content)
        
        vtt_path = save_vtt(sample, transcript)
        print(f"VTT subtitle saved to: {vtt_path}")

    except TranscriptionError as e:
        print(f"Transcription failed: {e}")