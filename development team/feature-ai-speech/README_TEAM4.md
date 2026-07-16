# Team 4 – AI & Speech Processing Module

## Module Overview

The AI & Speech Processing module is responsible for providing AI-powered content generation and speech-to-text functionality for the PAI-Project AI Video Editing SaaS backend.

This module integrates Google Gemini for AI content generation and OpenAI Whisper for audio transcription and subtitle generation.

---

# Features

## Google Gemini

- Secure API configuration using environment variables
- AI prompt processing
- Video title generation
- Video description generation
- Video summary generation
- Video editing suggestions
- Hashtag generation
- Retry mechanism
- Error handling

---

## Whisper

- Speech-to-text transcription
- Language detection
- Transcript generation
- JSON transcript export
- SRT subtitle generation
- VTT subtitle generation
- Error handling for unsupported files

---

# Folder Structure

```text
feature-ai-speech/

├── api_example.py
├── config.py
├── gemini_client.py
├── whisper_client.py
├── test_day2.py
├── sample.mp3
├── transcripts/
├── .env.example
└── README_TEAM4.md
```

---

# Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Required variables:

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-2.5-flash
WHISPER_MODEL_SIZE=base
```

Do **not** commit the `.env` file to GitHub.

---

# API Endpoints

## AI

| Method | Endpoint | Purpose |
|---------|----------|---------|
| POST | /ai/title | Generate video title |
| POST | /ai/description | Generate video description |
| POST | /ai/summary | Generate transcript summary |
| POST | /ai/editing-suggestions | Generate editing suggestions |
| POST | /ai/hashtags | Generate hashtags |

---

## Speech

| Method | Endpoint | Purpose |
|---------|----------|---------|
| POST | /speech/transcribe | Generate transcript and subtitles |

---

# External Dependencies

- FastAPI
- Uvicorn
- Google Gemini SDK
- OpenAI Whisper
- Torch
- Pydantic
- Python-dotenv

---

# Integration Guide

The backend team can import the API routes from `api_example.py` and integrate them into the main FastAPI application.

Whisper handles audio transcription, while Gemini generates AI-powered content from the transcript.

---

# Known Limitations

- Gemini requires a valid API key.
- Free-tier Gemini requests are subject to rate limits and quota restrictions.
- Whisper processing is CPU-based unless GPU support is available.
- The API example is designed for integration and should be merged into the main backend application.

---

# Future Improvements

- Database integration for transcript storage.
- Migration from `google.generativeai` to `google.genai`.
- Authentication for protected endpoints.
- Improved prompt templates.
- Additional subtitle formats.