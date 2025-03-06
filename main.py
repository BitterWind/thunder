from config import create_app
from routers import base, websocket, player

# 初始化应用
app = create_app()


# 注册路由
app.include_router(base.router)
app.include_router(websocket.router)
app.include_router(player.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)