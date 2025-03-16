from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from pydantic import Field

#用于初始化一个fastapi s
def create_app():
    app = FastAPI(
        title="游戏排行榜服务",
        description="基于FastAPI的实时排行榜系统",
        version="1.0.0"
    )
    # CORS 配置, 允许所有的IP地址访问该服务器。
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 挂载静态文件
    app.mount("/project", StaticFiles(directory="project"), name="project")

    return app

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()