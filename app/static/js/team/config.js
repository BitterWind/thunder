// 全局游戏配置, 一些与房间无关的东西，每房间都是一样的。

import { ip as IP } from '../lobby_config.js';
let ip = IP;
export const CONFIG = {
    PLAYER_SIZE         :30,
    BULLET_SPEED        :12,
    BULLET_SIZE         :12,//多排子弹的子弹间隔
    ENEMY_SPAWN_RATE    :0.05,
    FIRE_RATE           :15,// 毫秒
    ADD_SHOOTER_RATE    :1000,//增加护卫机的间隔
    SHOOTER_SPEED       :7,
    SHOOTER_RIDUS       :90,
    SHOOTER_LIMIT       :12,
    PLAYER_SPEED        :500,
    SEND_DATA           :"http://"+ip+"/player_data_cache/send_log_player",
    GET_DATA            :"http://"+ip+"/player_data_cache/get_log_player",
    GET_ID              :"http://"+ip+"/player_data_cache/get_id",
    SEND_SCORE          :"http://"+ip+"/player_data_memory/scores",
    GET_LEADERBOARD     :"http://"+ip+"/player_data_memory/leaderboard",
    GET_ROOM            :"http://"+ip+"/room_data_cache/get_room",
};

// 初始化游戏
export const canvas = document.getElementById('gameCanvas');

export const ctx = canvas.getContext('2d');

//游戏逻辑实体的队列
export const entities = {
    players: [],
    bullets: [],
    enemies: [],
    shooters1: [],
    shooters2: [],
    shooters3: [],
    shooters4: []
};

// 游戏配置
export let game_data = {
    bool                :false,                         //调试用的，避免发送过多消息
    mode                :1,                             //单人模式还是双人模式。
    name                :"我是你大爷",                   // 对的，暂时还不支持重复和空name，后续把id匹配上就好了。
    room                :0,                             //是的这里的东西应该是可以修改的
    id           :0,                             //在第一次接收数据的时候由服务器生成，这里需要一个最小堆。
    team_member         :{"name":"guy2", "id":152},
    time_cnt            :0,
    score               :0
};

// 在 config.js 中添加
// 添加 game_state 的定义和导出
// 修改为4人状态配置
export let game_state = {
    score: 0,
    maxScore: 0,
    players: [ // 数组长度改为4
        { id: 1, score: 0, active: true },
        { id: 2, score: 0, active: true },
        { id: 3, score: 0, active: true },
        { id: 4, score: 0, active: true }
    ],
    maxPlayers: 4, // 新增最大玩家数
    currentTurn: 0  // 当前回合索引（0-3）
};