from google import genai

from ..config import get_settings

settings = get_settings()

client = None

if settings.google_api_key:
    client = genai.Client(
        api_key=settings.google_api_key
    )


def update_workout_plan(
    original_plan: str,
    feedback: str,
) -> str:
    """
    Update the original workout plan based on user feedback.
    """

    if not settings.google_api_key or client is None:
        return (
            "Gemini API key is not configured. "
            "Please add GOOGLE_API_KEY to the .env file."
        )

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Here is the original workout plan:

{original_plan}

User feedback:

{feedback}

Create an updated workout plan based on the user's feedback.

Requirements:
- Keep the plan personalized.
- Modify the workout according to the feedback.
- Keep a clear 7-day structure where possible.
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
        return f"Unable to update workout plan: {exc}"