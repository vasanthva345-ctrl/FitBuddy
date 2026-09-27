import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = "FitBuddy - AI Fitness Plan Generator"
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")


def get_settings():
    return Settings()