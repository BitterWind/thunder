from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal
from security import get_password_hash, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="./templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "error_message": msg}
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error_message": msg}
    )


@router.post("/login")
async def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": "无效的用户名或密码"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error_message": msg}
    )


@router.post("/register")
async def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error_message": "用户名已存在"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    hashed_password = get_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()

    return RedirectResponse(
        url="/login?msg=注册成功，请登录",
        status_code=status.HTTP_303_SEE_OTHER
    )