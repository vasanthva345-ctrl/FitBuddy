import google.generativeai as genai
from app.config import get_settings

settings = get_settings()

genai.configure(api_key=settings.google_api_key)

for model in genai.list_models():
    print(model.name)