from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from routes.auth import router as auth_router
from routes.game import router as game_router
from routes.sse import router as sse_router
from routes.multiGame import router as multiGame_router
from database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.room_cleaner import room_cleanup  # 导入清理函数
import asyncio
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 全局异常处理器注册必须在所有路由导入之前
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "参数验证失败"}
    )


# 添加 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# 包含路由
app.include_router(auth_router)
app.include_router(game_router)

app.include_router(sse_router)
app.include_router(multiGame_router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")


'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)'''


from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    # 每5分钟执行一次清理房间
    scheduler.add_job(room_cleanup, 'interval', minutes=5)
    scheduler.start()

'''
def run_app(port):
    asyncio.run(uvicorn.run(app, host="127.0.0.1", port=port))

if __name__ == "__main__":
    # 在端口8000和8001上启动FastAPI应用程序
    run_app(8000)
    run_app(8001)'''

import subprocess

# 运行第一个进程（端口8000）
subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])

# 运行第二个进程（端口8001）
subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"])

