// 全局游戏配置
export const CONFIG = {
    PLAYER_SIZE: 30,
    BULLET_SPEED: 12,
    BULLET_SIZE: 12,//多排子弹的子弹间隔
    ENEMY_SPAWN_RATE: 0.05,
    FIRE_RATE: 15,// 毫秒
    ADD_SHOOTER_RATE:1000,//增加护卫机的间隔
    SHOOTER_SPEED:7,
    SHOOTER_RIDUS:90,
    SHOOTER_LIMIT:12,
    PLAYER_SPEED:500,
    SEND_DATA:"http://localhost:8000/send-log-player",
    GET_DATA:"http://localhost:8000/get-log-player",
    GET_ID:"http://localhost:8000/send-id"
};

// 初始化游戏
export const canvas = document.getElementById('gameCanvas');

export const ctx = canvas.getContext('2d');

//游戏逻辑实体的队列
export const entities = {
    players: [],
    bullets: [],
    enemies: [],
    Shooters1: [],
    Shooters2: []
};

// 游戏配置
export const gameState = {
    bool: false,//调试用的，避免发送过多消息
    mode: 1,//单人模式还是双人模式。
    name: "0",// 对的，暂时还不支持重复和空name，后续把id匹配上就好了。
    playerID: 0,//在第一次接收数据的时候由服务器生成，这里需要一个最小堆。
    teamMember: "NULL",
    timeCnt: 0,
    playerCnt: 1,//玩家数量
};