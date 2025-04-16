from config import create_app
from routers import  websocket, player, redis, auth, room
from fastapi.staticfiles import StaticFiles
from data_bases.SQLite import Base, engine

Base.metadata.create_all(bind=engine)
# 初始化应用
app = create_app()

# 注册路由
app.include_router(websocket.router)
app.include_router(player.router)
app.include_router(redis.router)
app.include_router(room.router)
app.include_router(auth.router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)

