"""
Example FastAPI endpoints for Team 4 - AI & Speech Processing.

This file demonstrates how the AI & Speech module can be integrated
into the backend API. It can later be merged into the main backend
application by the backend team.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from gemini_client import (
    generate_title,
    generate_description,
    generate_summary,
    generate_editing_suggestions,
    generate_hashtags,
)

from whisper_client import (
    transcribe_audio,
    save_transcript,
    save_srt,
    save_vtt,
    TranscriptionError,
)

from gemini_client import GeminiError

app = FastAPI(title="PAI Project - AI & Speech API")

class PromptRequest(BaseModel):
    transcript: str


class AudioRequest(BaseModel):
    file_path: str
    
@app.post("/ai/title")
def ai_title(request: PromptRequest):
    try:
        title = generate_title(request.transcript)
        return {
            "success": True,
            "title": title
        }
    except GeminiError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/description")
def ai_description(request: PromptRequest):
    try:
        description = generate_description(request.transcript)
        return {
            "success": True,
            "description": description
        }
    except GeminiError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/summary")
def ai_summary(request: PromptRequest):
    try:
        summary = generate_summary(request.transcript)
        return {
            "success": True,
            "summary": summary
        }
    except GeminiError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/editing-suggestions")
def ai_editing_suggestions(request: PromptRequest):
    try:
        suggestions = generate_editing_suggestions(request.transcript)
        return {
            "success": True,
            "editing_suggestions": suggestions
        }
    except GeminiError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/hashtags")
def ai_hashtags(request: PromptRequest):
    try:
        hashtags = generate_hashtags(request.transcript)
        return {
            "success": True,
            "hashtags": hashtags
        }
    except GeminiError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/speech/transcribe")
def speech_transcribe(request: AudioRequest):
    try:
        transcript = transcribe_audio(request.file_path)

        json_path = save_transcript(request.file_path, transcript)
        srt_path = save_srt(request.file_path, transcript)
        vtt_path = save_vtt(request.file_path, transcript)

        return {
            "success": True,
            "language": transcript["language"],
            "transcript": transcript["text"],
            "json_file": json_path,
            "srt_file": srt_path,
            "vtt_file": vtt_path
        }

    except TranscriptionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def home():
    return {
        "message": "PAI Project AI & Speech Processing API",
        "status": "running"
    }