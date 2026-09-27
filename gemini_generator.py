from google import genai

from ..config import get_settings

settings = get_settings()

client = None

if settings.google_api_key:
    client = genai.Client(
        api_key=settings.google_api_key
    )


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    """
    Generate a personalized 7-day workout plan using Gemini.
    """

    if not settings.google_api_key or client is None:
        return (
            "Gemini API key is not configured. "
            "Please add GOOGLE_API_KEY to the .env file."
        )

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Create a personalized 7-day workout plan for the following user:

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Requirements:
- Create a clear 7-day workout schedule.
- Include exercises for each day.
- Include sets, repetitions, or duration where appropriate.
- Include rest/recovery days where appropriate.
- Keep the plan suitable for the user's selected intensity.
- Keep the response practical and easy to follow.
- Do not provide medical diagnosis or treatment.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=prompt,
        )

        return response.text

    except Exception as exc:
        return f"Unable to generate workout plan: {exc}"