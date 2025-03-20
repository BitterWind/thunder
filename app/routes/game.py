from typing import Dict

from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal
from security import get_password_hash, verify_password
from starlette.responses import JSONResponse

from .auth import get_db

router = APIRouter()
templates = Jinja2Templates(directory="./templates")


@router.get("/game", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    # 检查用户是否已登录
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
        # 获取用户数据
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    return templates.TemplateResponse(
        "game.html",
        {"request": request, "username": username, "maxScore": user.maxScore}
    )

@router.post("/scores", response_model=dict, status_code=201, summary="提交分数并返回排名")
async def submit_score(data: Dict, db: Session = Depends(get_db)):
    try:
        print(data)
        user_name = data.get("username")
        score = data.get("score")

        if user_name is None or score is None:
            raise HTTPException(status_code=400, detail="用户ID或分数缺失")

        # 查询用户
        user = db.query(User).filter(User.username == user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户未找到")

        # 更新用户分数
        if score > user.maxScore:
            user.maxScore = score

        db.commit()

        return {
            "username": user_name,
            "score": score,
            "message": "分数更新成功"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@router.get("/room", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    # 检查用户是否已登录
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
        # 获取用户数据
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    return templates.TemplateResponse(
        "room.html",
        {"request": request, "username": username, "maxScore": user.maxScore}
    )

@router.get("/setup", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    # 检查用户是否已登录
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
        # 获取用户数据
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    return templates.TemplateResponse(
        "setup.html",
        {"request": request, "username": username, "maxScore": user.maxScore}
    )