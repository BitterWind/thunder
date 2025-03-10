from config import create_app
from routers import basic, websocket, player, redis
# 初始化应用
app = create_app()

# 注册路由
app.include_router(basic.router)
app.include_router(websocket.router)
app.include_router(player.router)
app.include_router(redis.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.91.1", port=8000)