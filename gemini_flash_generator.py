from google import genai

from ..config import get_settings

settings = get_settings()

client = None

if settings.google_api_key:
    client = genai.Client(
        api_key=settings.google_api_key
    )


def generate_nutrition_tip_with_flash(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    """
    Generate a personalized nutrition tip using Gemini Flash.
    """

    if not settings.google_api_key or client is None:
        return (
            "Gemini API key is not configured. "
            "Please add GOOGLE_API_KEY to the .env file."
        )

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Provide a concise personalized nutrition tip for:

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Requirements:
- Give practical nutrition guidance.
- Keep it easy to understand.
- Consider the user's fitness goal and workout intensity.
- Do not provide medical diagnosis or treatment.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        return response.text

    except Exception as exc:
        return f"Unable to generate nutrition tip: {exc}"