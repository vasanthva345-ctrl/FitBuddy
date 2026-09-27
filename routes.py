from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .database import (
    get_all_plans,
    get_all_users,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)

from .ai.gemini_generator import generate_workout_gemini
from .ai.gemini_flash_generator import generate_nutrition_tip_with_flash
from .ai.updated_plan import update_workout_plan


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class UserInput(BaseModel):
    username: str
    user_id: str
    age: int
    weight: float
    goal: str
    intensity: str


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        },
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    user_input = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    existing_user = get_user(user_input.user_id)

    if not existing_user:
        save_user(
            user_id=user_input.user_id,
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
        )

    workout_plan = generate_workout_gemini(
        username=user_input.username,
        age=user_input.age,
        weight=user_input.weight,
        goal=user_input.goal,
        intensity=user_input.intensity,
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        username=user_input.username,
        age=user_input.age,
        weight=user_input.weight,
        goal=user_input.goal,
        intensity=user_input.intensity,
    )

    save_plan(
        user_id=user_input.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user_input,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
        },
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    original_plan = get_original_plan(user_id)

    if not original_plan:
        return HTMLResponse(
            content="Original workout plan not found.",
            status_code=404,
        )

    updated_plan = update_workout_plan(
        original_plan=original_plan,
        feedback=feedback,
    )

    update_plan(
        user_id=user_id,
        updated_plan=updated_plan,
    )

    user = get_user(user_id)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "workout_plan": updated_plan,
            "nutrition_tip": "Updated based on your feedback.",
        },
    )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "plans": plans,
        },
    )

@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "plans": plans,
        },
    )