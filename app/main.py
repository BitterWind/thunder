from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.auth import router as auth_router
from routes.game import router as game_router
from database import Base, engine
from starlette.middleware.sessions import SessionMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.room_cleaner import room_cleanup  # 导入清理函数

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 添加 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# 包含路由
app.include_router(auth_router)
app.include_router(game_router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")


'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.91.1", port=8000)'''


from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    # 每5分钟执行一次清理房间
    scheduler.add_job(room_cleanup, 'interval', minutes=5)
    scheduler.start()
