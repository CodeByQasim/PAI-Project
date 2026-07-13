"""
Gemini API integration for PAI-Project (Team 4 - AI & Speech Processing)

Day 1: connection setup (done)
Day 2: send a sample prompt, receive a response (done below)
Day 3: error handling + retry for API edge cases (done below)
"""

import time
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


class GeminiError(Exception):
    """Raised when Gemini fails after all retries."""
    pass


def _get_model():
    return genai.GenerativeModel(GEMINI_MODEL)


def test_connection():
    """Quick sanity check that the API key + model name are valid."""
    try:
        model = _get_model()
        response = model.generate_content("Say 'Gemini is connected.'")
        print(response.text.strip())
        return True
    except Exception as e:
        print(f"Gemini connection failed: {e}")
        return False


def send_prompt(prompt: str, max_retries: int = 3, backoff_seconds: float = 2.0) -> str:
    """
    Send a prompt to Gemini and return the text response.
    Retries on transient errors (rate limits, network blips) with exponential backoff.
    Raises GeminiError if it still fails after max_retries.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    model = _get_model()
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(prompt)

            # Edge case: Gemini can return a response object with no usable text
            # (e.g. blocked by safety filters) - .text raises in that case
            if not response.candidates:
                raise GeminiError("Gemini returned no candidates (likely blocked by safety filters)")

            text = response.text
            if not text or not text.strip():
                raise GeminiError("Gemini returned an empty response")

            return text.strip()

        except GeminiError:
            raise  # don't retry on content/safety issues, only transient ones
        except Exception as e:
            last_error = e
            error_str = str(e).lower()

            # Non-retryable errors - fail fast instead of wasting retries
            if "api key" in error_str or "permission" in error_str or "404" in error_str:
                raise GeminiError(f"Non-retryable Gemini error: {e}")

            if attempt < max_retries:
                wait = backoff_seconds * (2 ** (attempt - 1))
                print(f"Gemini call failed (attempt {attempt}/{max_retries}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise GeminiError(f"Gemini failed after {max_retries} attempts: {last_error}")

def generate_title(transcript: str) -> str:
    """
    Generate a short, engaging title from a transcript.
    """
    prompt = f"""
Generate a short and engaging video title (maximum 10 words)
based on the following transcript.

Transcript:
{transcript}

Return only the title.
"""
    return send_prompt(prompt)


def generate_description(transcript: str) -> str:
    """
    Generate a YouTube-style video description.
    """
    prompt = f"""
Write a professional video description based on this transcript.

Transcript:
{transcript}

Return only the description.
"""
    return send_prompt(prompt)


def generate_summary(transcript: str) -> str:
    """
    Generate a concise summary of the transcript.
    """
    prompt = f"""
Summarize the following transcript in 2-3 sentences.

Transcript:
{transcript}
"""
    return send_prompt(prompt)

if __name__ == "__main__":
    # Day 1 check
    if test_connection():
        # Day 2 deliverable: send a sample prompt, receive a response
        sample_prompt = "In one sentence, explain what an AI video editing SaaS backend does."
        try:
            result = send_prompt(sample_prompt)
            print("\nSample prompt:", sample_prompt)
            print("Gemini response:", result)
        except GeminiError as e:
            print(f"Could not get a response: {e}")