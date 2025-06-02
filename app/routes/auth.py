from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.user import User
from security import get_password_hash, verify_password
from starlette.responses import JSONResponse

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="./templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 检查用户是否已登录
def get_current_user(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未认证的用户"
        )
    return username


@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.maxScore.desc()).all()
    # 将用户数据转换为列表字典格式
    leaderboard_data = [{"username": user.username, "maxScore": user.maxScore} for user in users]
    return JSONResponse(content={"users": leaderboard_data})
'''
# 获取排行榜数据
@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard(request: Request, db: Session = Depends(get_db)):
    # 查询所有用户并按 maxScore 降序排序
    users = db.query(User).order_by(User.maxScore.desc()).all()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "leaderboard": users}
    )
'''

@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, msg: str = None):
    # 检查用户是否已登录
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
        # 获取用户数据
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "username": username, "maxScore": user.maxScore}
    )

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error_message": msg}
    )
@router.post("/")
async def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": "该用户不存在"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    elif not verify_password(form_data.password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": "密码错误"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    # 生成访问令牌
    #access_token = create_access_token(data={"sub": user.username})
    # 将用户数据保存到 Session
    request.session["username"] = user.username
    request.session["maxScore"] = user.maxScore

    # 重定向到 home 页面
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

# 注销逻辑
@router.get("/logout")
async def logout(request: Request):
    # 清除 Session 中的用户数据
    request.session.pop("username", None)
    request.session.pop("maxScore", None)
    return RedirectResponse(url="/")

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
        url="/?msg=注册成功，请登录",
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.get("/profile")
async def logout(request: Request):
    # 检查用户是否已登录
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
        # 获取用户数据
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": username, "maxScore": user.maxScore}
    )


# 新增路由 - 修改密码
@router.post("/change-password", response_class=JSONResponse)
async def change_password(
        request: Request,
        old_password: str = Form(...),
        new_password: str = Form(...),
        confirm_password: str = Form(...),
        db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return JSONResponse(status_code=401, content={"message": "未认证的用户"})

    user = db.query(User).filter(User.username == username).first()

    if not verify_password(old_password, user.password_hash):
        return JSONResponse(status_code=400, content={"message": "旧密码错误"})

    if new_password != confirm_password:
        return JSONResponse(status_code=400, content={"message": "新密码不一致"})

    user.password_hash = get_password_hash(new_password)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "密码更新成功"})

# 新增路由 - 修改用户名
@router.post("/change-username", response_class=JSONResponse)
async def change_username(
        request: Request,
        new_username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return JSONResponse(status_code=401, content={"message": "未认证的用户"})

    user = db.query(User).filter(User.username == username).first()
    if not verify_password(password, user.password_hash):
        return JSONResponse(status_code=400, content={"message": "密码错误"})

    existing_user = db.query(User).filter(User.username == new_username).first()
    if existing_user:
        return JSONResponse(status_code=400, content={"message": "用户名已存在"})

    user.username = new_username
    db.commit()

    request.session["username"] = new_username

    return JSONResponse(status_code=200, content={"message": "用户名更新成功"})

