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

import asyncio

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


# 新增路由处理 /waiting/{room_id}
@router.get("/waiting/{room_id}", response_class=HTMLResponse)
async def waiting_room(
        request: Request,
        room_id: int,
        db: Session = Depends(get_db)
):
    # 验证用户登录状态
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/")

    # 获取用户和房间信息
    user = db.query(User).filter(User.username == username).first()
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        return RedirectResponse(url="/room")

    # 验证用户是否在房间内
    if user.room_id != room_id:
        return RedirectResponse(url="/room")

    return templates.TemplateResponse(
        "waiting.html",
        {
            "request": request,
            "username": username,
            "room": room,
            "maxScore": user.maxScore
        }
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
        raise HTTPException(404, "用户不存在")

    creator_id = current_user.id
    name = data.get("name")
    password = data.get("password")

    if not name:
        raise HTTPException(400, "房间名称不能为空")

    # 检查用户是否已在房间
    if current_user.room_id:
        raise HTTPException(409, "请先退出当前房间")

    # 检查房间名唯一性
    existing_room = db.query(Room).filter(Room.name == name).first()
    if existing_room:
        raise HTTPException(409, "房间名称已存在")

    # 创建房间
    new_room = Room(
        name=name,
        #mode=mode,
        password=password,
        creator_id=current_user.id,
        current_players=1,
        max_players=4,
        status="waiting"
    )



    db.add(new_room)
    db.flush()  # 预提交获取房间ID

    # 关联用户到房间
    current_user.room_id = new_room.id

    db.commit()
    db.refresh(new_room)

    return JSONResponse(content={
        "redirect": f"/waiting/{new_room.id}",
        "message": "房间创建成功",
        "room": new_room.to_dict()
    })



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
            raise HTTPException(404, "用户不存在")

        # 获取请求参数
        room_name = data.get("roomName")
        password = data.get("password", "")

        # 查询目标房间
        target_room = db.execute(
            select(Room).where(Room.name == room_name)
        ).scalar_one_or_none()

        if not target_room:
            raise HTTPException(400, "需要指定房间名称")

        # 检查用户是否已在房间
        if current_user.room_id:
            existing_room = db.get(Room, current_user.room_id)
            if existing_room and existing_room.name == room_name:
                return {
                    "redirect": f"/waiting/{existing_room.id}",
                    "message": "加入成功",
                    "room_id": existing_room .id,
                    "player_count": existing_room .current_players
                }
            msg = f"您已在房间 {existing_room.name} 中"
            raise HTTPException(409, msg)


        # 房间状态验证
        target_room = db.execute(
            select(Room)
            .where(Room.name == room_name)
            .with_for_update()  # 行级锁防止并发问题
        ).scalar_one_or_none()

        if not target_room:
            raise HTTPException(404, "房间不存在")
        if target_room.status != "waiting":
            raise HTTPException(403, "房间已开始游戏")
        if target_room.current_players >= target_room.max_players:
            raise HTTPException(409, "房间人数已满")

        # 验证密码
        if target_room.password and target_room.password != password:
            raise HTTPException(403, "密码错误")



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
            "redirect": f"/waiting/{target_room.id}",
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
    return {"redirect": "/room",}


# 房间状态轮询接口
@router.get("/room/{room_id}/status")
async def get_room_status(
        room_id: int,
        db: Session = Depends(get_db)
):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(404, "房间不存在")

    return room.to_dict()


# 开始游戏检查
@router.post("/room/{room_id}/start")
async def start_game_check(
        room_id: int,
        db: Session = Depends(get_db)
):
    room = db.query(Room).get(room_id)
    if room.current_players < room.max_players:
        raise HTTPException(400, "玩家人数不足")

    # 更新房间状态
    room.status = "ready"
    db.commit()

    return {"status": "ready"}


# 内存存储实时状态
active_rooms = {}  # {room_id: {"countdown": int, "listeners": set}}




@router.post("/room/{room_id}/ready")
async def toggle_ready_status(
        request: Request,
        room_id: int,
        db: Session = Depends(get_db),
        #username: str = "当前用户"  # 需替换为实际认证方式
):
    # 获取当前用户
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(404, "用户不存在")

    room = db.query(Room).filter(Room.id == room_id).first()

    # 切换准备状态
    user.ready_status = not user.ready_status
    db.commit()

    # 检查是否全部准备就绪
    players = db.query(User).filter(User.room_id == room_id).all()

    if room.current_players < room.max_players:
        return {"ready_status": user.ready_status}
    if all(p.ready_status for p in players):
        await start_countdown(room_id, db)

    return {"ready_status": user.ready_status}


async def start_countdown(room_id: int, db: Session):
    """开始倒计时协程"""
    room = db.query(Room).get(room_id)
    if not room:
        return

    try:
        # 更新房间状态
        room.status = "ready"
        db.commit()

        # 执行5秒倒计时
        for i in range(5, 0, -1):
            room.countdown = i
            db.commit()
            await asyncio.sleep(1)
            notify_listeners(room_id)  # 通知监听者

        # 跳转游戏场景
        room.status = "in_game"
        db.commit()

    finally:
        # 清理状态
        active_rooms.pop(room_id, None)
        db.close()

def notify_listeners(room_id: int):
    """通知所有监听客户端（需配合SSE实现）"""
    # 此处需要与SSE推送机制配合
    pass


@router.get("/room/{room_id}/players")
async def get_room_players(
        request: Request,
        room_id: int,
        db: Session = Depends(get_db),
):
    """获取房间玩家列表"""
    # 验证用户权限
    # 获取当前用户
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/")

    user = db.query(User).filter(User.username == username).first()


    if not user or user.room_id != room_id:
        raise HTTPException(status_code=403, detail="无权查看该房间")

    # 查询房间信息
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    # 获取所有玩家
    players = db.query(User).filter(User.room_id == room_id).all()



    return [{
        "name": p.username,
        "ready": p.ready_status,
        "max_score": p.maxScore,
        "is_creator": p.id == room.creator_id
    } for p in players]