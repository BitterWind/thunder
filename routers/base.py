from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

#this file is bound for hanging files 
@router.get("/")
async def main():
    return {"message": "访问/client.html 或者/game.html 开始游戏"}

@router.get("/client.html")
async def client():
    return FileResponse('static/client.html')

@router.get("/game.html")
async def game():
    return FileResponse('static/game.html')
