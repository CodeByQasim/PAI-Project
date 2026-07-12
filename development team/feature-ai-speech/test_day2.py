"""
End-to-end test for Team 4 (AI & Speech) Day 2/3 deliverables.
Run this to check off: Gemini connection working, Whisper transcription working,
sample transcript generated, error handling in place.

Usage: python test_day2.py
"""

from gemini_client import test_connection, send_prompt, GeminiError
from whisper_client import transcribe_audio, save_transcript, TranscriptionError

SAMPLE_AUDIO = "sample.mp3"
SAMPLE_PROMPT = "In one sentence, explain what an AI video editing SaaS backend does."


def run():
    print("=" * 50)
    print("TEAM 4 - AI & SPEECH - Day 2/3 test run")
    print("=" * 50)

    # 1. Gemini connection
    print("\n[1/3] Testing Gemini connection...")
    if not test_connection():
        print("Stopping: fix Gemini connection before continuing.")
        return

    # 2. Gemini sample prompt -> response
    print("\n[2/3] Sending sample prompt to Gemini...")
    try:
        response = send_prompt(SAMPLE_PROMPT)
        print(f"Prompt:   {SAMPLE_PROMPT}")
        print(f"Response: {response}")
    except GeminiError as e:
        print(f"Gemini prompt failed: {e}")

    # 3. Whisper transcription + save
    print(f"\n[3/3] Transcribing '{SAMPLE_AUDIO}' and saving transcript...")
    try:
        transcript = transcribe_audio(SAMPLE_AUDIO)
        saved_path = save_transcript(SAMPLE_AUDIO, transcript)
        print(f"Language: {transcript['language']}")
        print(f"Text: {transcript['text']}")
        print(f"Saved to: {saved_path}")
    except TranscriptionError as e:
        print(f"Whisper transcription failed: {e}")

    print("\nDone.")


if __name__ == "__main__":
    run()