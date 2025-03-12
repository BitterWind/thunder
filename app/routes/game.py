from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal
from security import get_password_hash, verify_password
from starlette.responses import JSONResponse


router = APIRouter()
templates = Jinja2Templates(directory="./templates")


@router.get("/game", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error_message": msg}
    )