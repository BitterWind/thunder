from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
#只在分发界面的时候使用get，数据方面使用post
#this file is bound for hanging files 

# @router.get("/")
# async def main():
#     return {"message": "访问/client.html登录 或者/game.html 开始游戏"}

# 这个界面很可能用来登录？
@router.get("/client.html")
async def client():
    return FileResponse('project/client.html')
@router.get("/favicon.ico ")
async def favicon():
    return FileResponse('project/favicon.ico')
@router.get("/game.html")
async def game1():
    return FileResponse('project/index.html')
@router.get("/css/style.css")
async def game2():
    return FileResponse('project/css/style.css')
@router.get("/js/config.js")
async def game3():
    return FileResponse('project/js/config.js')
@router.get("/js/classes.js")
async def game4():
    return FileResponse('project/js/classes.js')
@router.get("/js/input.js")
async def game5():
    return FileResponse('project/js/input.js')
@router.get("/js/network.js")
async def game6():
    return FileResponse('project/js/network.js')
@router.get("/js/gameLogic.js")
async def game7():
    return FileResponse('project/js/gameLogic.js')
@router.get("/js/main.js")
async def game8():
    return FileResponse('project/js/main.js')
