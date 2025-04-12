网络应用系统开发课程的课程大作业
仿雷霆战机编写的一个全栈小游戏
服务器使用fastapi框架
数据库，暂时采用aqlite，但常用的数据还是用程序中的各种变量
数据分发服务器，反向代理服务器，都在计划中
网络层用websocket，
把双人模式登录界面和双人模式做完后我就等到快要验收的时候再去补充特效之类的东西好了。
github desktop 集成了git的功能，对于初学者的使用而言，很好用了。
文件介绍
--thunder 仿制雷霆战机做一个小游戏
    --data_bases   
        --redis.py  ：  就一个函数，函数功能是与数据库建立连接，routers/redis.py 中有较多的应用
    --models
        --schemas.py : 一些数据类型，没排上什么用处， 后续准备全部拿字典替代 。
    --project 
        --css
            --style.css : index.html 的 外部样式配置
        --js : index.html 中import的外部包和代码段落的目录工具。
            --classes.js 游戏逻辑中出现的各种游戏主体，如子弹，敌机及其配套函数的。
            --config.js  游戏逻辑处理中出现的各种全局变量配置。
            --gamelogic.js 游戏逻辑，包括事件检测，渲染和游戏实体数据更新。
            --imput.js    游戏过程中涉及到的输入处理，主要是各种事件的监听。
            --main.js    游戏逻辑和index.html的功能大差不差。
            --network.js  用于发送和接收与服务器相关的数据，例如id，room_number等。
            --client.html 目前的登录前端，待废除。
            --index.html  目录工具。
    --routers :各种各样的路由，用来接收项目传来的数据并返回请求
        --basic.py 用于主要页面的传输，实际上只要把client.html 和 index.html传过去整个项目就能传过去。
        --player.py 玩家相关数据的传输。
        --redis.py  数据库相关内容的处理，主要是排行榜的内容。
        --tmp.py  临时文件。
        --websocket.py 没什么用，后续废除。
    --services 
        --game_service.py 主要是game_services这个结构体的相关处理，这个结构体处理所有玩家的数据。、
    --config.py 配置fastapi的服务器。
    --main.py  启动服务器，挂载路由。

具体逻辑
server.py -- login request      -- login -- home page -- game page -- web player init   -- upload/receive data  
            |                  |                                   |                    |
            -- SQLite make sure                                    -- server player init