from config import create_app
from routers import basic, websocket, player, redis, auth
from fastapi.staticfiles import StaticFiles

# 初始化应用
app = create_app()

# 注册路由
app.include_router(basic.router)
app.include_router(websocket.router)
app.include_router(player.router)
app.include_router(redis.router)
app.include_router(auth.router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.91.1", port=8000)

