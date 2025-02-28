#之后可以和server.py整合一下
from fastapi import FastAPI, Form, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import inspect
import bcrypt

# 配置数据库
DATABASE_URL = "sqlite:///./test.db"
app = FastAPI()

# SQLAlchemy模型基础类
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    failed_attempts = Column(Integer, default=0)  # 用于记录登录失败次数
    lock_until = Column(DateTime, nullable=True)  # 用于记录账户锁定时间

# 数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Jinja2模板
templates = Jinja2Templates(directory="templates")

# 创建表格
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

# 注册页面
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 登录页面
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 注册处理
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    # 检查用户名是否已经存在
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # 密码加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 保存用户到数据库
    new_user = User(username=username, hashed_password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return RedirectResponse(url="/login", status_code=303)

# 登录处理
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    db_user = db.query(User).filter(User.username == username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # 检查账户是否被锁定
    if db_user.lock_until and db_user.lock_until > datetime.now():
        # 账户被锁定，返回错误信息
        lock_duration = db_user.lock_until - datetime.now()
        raise HTTPException(
            status_code=403,
            detail=f"Account locked. Try again after {lock_duration.seconds // 60} minutes."
        )
    
    # 验证密码
    if not bcrypt.checkpw(password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        # 密码错误，增加失败次数
        db_user.failed_attempts += 1
        
        if db_user.failed_attempts >= 5:
            # 如果失败次数达到 5 次，锁定账户 30 分钟
            db_user.lock_until = datetime.now() + timedelta(minutes=30)
            db_user.failed_attempts = 0  # 重置失败次数

        db.commit()
        db.refresh(db_user)

        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # 如果密码正确，重置失败次数和锁定时间
    db_user.failed_attempts = 0
    db_user.lock_until = None
    db.commit()
    db.refresh(db_user)
    
    db.close()
    
    return {"message": f"Welcome back, {username}!"}

# 首页
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 启动时确认数据库连接
@app.get("/check_db")
def check_db():
    # 检查数据库是否存在用户表
    inspector = inspect(engine)
    if "users" in inspector.get_table_names():
        return {"message": "Users table exists!"}
    else:
        return {"message": "Users table does not exist!"}
