// 全局游戏配置
let ip = "192.168.91.1:8000"
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
    SEND_DATA       :"http://"+ip+"/player_data_cache/send_log_player",
    GET_DATA        :"http://"+ip+"/player_data_cache/get_log_player",
    GET_ID          :"http://"+ip+"/player_data_cache/get_id",
    SEND_SCORE      :"http://"+ip+"/player_data_memory/scores",
    GET_LEADERBOARD :"http://"+ip+"/player_data_memory/leaderboard",
    GET_ROOM        :"http://"+ip+"/player_data_cache/get_room"
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
    shooters2: []
};

// 游戏配置
export let game_state = {
    bool: false,//调试用的，避免发送过多消息
    mode: 1,//单人模式还是双人模式。
    name: "我是你大爷",// 对的，暂时还不支持重复和空name，后续把id匹配上就好了。
    room: 0, //是的这里的东西应该是可以修改的
    player_id: 0,//在第一次接收数据的时候由服务器生成，这里需要一个最小堆。
    team_member: "NULL",
    time_cnt: 0,
    score: 0
};