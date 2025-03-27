from typing import Dict
from fastapi import Body
from sqlalchemy import select
from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.user import User
from models.room import Room
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
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

# 获取房间列表
@router.get("/rooms", response_class=HTMLResponse)
async def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return JSONResponse(content={"rooms": [room.to_dict() for room in rooms]})


# 创建房间
@router.post("/create-room", response_class=HTMLResponse)
async def create_room(
    request: Request,
    data: Dict,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/")

    current_user = db.query(User).filter(User.username == username).first()
    if not current_user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "用户不存在"}
        )

    creator_id = current_user.id
    name = data.get("name")
    password = data.get("password")

    if not name:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "房间名称不能为空"}
        )

    # 检查房间名唯一性
    existing_room = db.query(Room).filter(Room.name == name).first()
    if existing_room:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "房间名称已存在"}
        )

    # 创建房间
    new_room = Room(
        name=name,
        #mode=mode,
        password=password,
        creator_id=current_user.id,
        current_players=1,
        max_players=6,
        status="preparing"
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return JSONResponse(content={"message": "房间创建成功", "room": new_room.to_dict()})


# 加入房间
@router.post("/join-room")
async def join_room(
        request: Request,
        data: Dict,
        db: Session = Depends(get_db)
):

    try:
        # 获取当前用户
        username = request.session.get("username")
        if not username:
            return RedirectResponse(url="/")

        current_user = db.query(User).filter(User.username == username).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 获取请求参数
        room_name = data.get("roomName")
        password = data.get("password", "")

        # 查询目标房间
        target_room = db.execute(
            select(Room).where(Room.name == room_name)
        ).scalar_one_or_none()

        if not target_room:
            raise HTTPException(status_code=404, detail="房间不存在")

        # 检查房间状态
        if target_room.status != "preparing":
            raise HTTPException(status_code=403, detail="房间已开始游戏")

        # 验证密码
        if target_room.password and target_room.password != password:
            raise HTTPException(status_code=403, detail="密码错误")

        # 检查人数限制
        if target_room.current_players >= target_room.max_players:
            raise HTTPException(status_code=409, detail="房间已满")

        # 检查用户是否已在房间
        if current_user.room_id is not None:
            raise HTTPException(status_code=409, detail="你已经在其他房间")

        # 执行加入操作（事务保证原子性）
        with db.begin_nested():
            # 更新用户房间关联
            current_user.room_id = target_room.id
            # 更新房间人数
            target_room.current_players += 1

            # 如果房间首次加入，设置创建者
            if not target_room.creator_id:
                target_room.creator_id = current_user.id

        db.commit()

        return {
            "message": "加入成功",
            "room_id": target_room.id,
            "player_count": target_room.current_players
        }

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

#离开房间，暂未调用
@router.post("/leave-room")
async def leave_room(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/")
    user = db.query(User).filter(User.username == username).first()  # 需要实现用户获取逻辑
    if user.room_id is None:
        raise HTTPException(400, "未加入任何房间")

    room = db.get(Room, user.room_id)
    with db.begin_nested():
        user.room_id = None
        room.current_players -= 1
        if room.current_players == 0:
            db.delete(room)
    db.commit()
    return {"message": "已离开房间"}


