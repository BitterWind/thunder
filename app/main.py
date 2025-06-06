from config import create_app
from routers import  websocket, player, redis1,  room
from fastapi.staticfiles import StaticFiles
from data_bases.SQLite import Base, engine
from fastapi.templating import Jinja2Templates
from routes.auth import router as auth_router
from routes.game import router as game_router
from routes.sse import router as sse_router
from routes.multiGame import router as multiGame_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException

Base.metadata.create_all(bind=engine)
# 初始化应用
app = create_app()


# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有 headers
)

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


# 注册路由
app.include_router(websocket.router)
app.include_router(player.router)
app.include_router(redis1.router)
app.include_router(room.router)
app.include_router(auth_router)
app.include_router(game_router)
app.include_router(sse_router)
app.include_router(multiGame_router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/project", StaticFiles(directory="project"), name="project")

templates = Jinja2Templates(directory="./templates")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



