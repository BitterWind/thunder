import { entities, canvas } from './config.js';
import { initInput } from './input.js';
import { gameLoop } from './gameLogic.js';
import { Player } from './classes.js';
import { idRequest } from './network.js';

// 初始化玩家
entities.players.push(new Player(idRequest()));
// entities.players.push(new Player(1));
// document.write("fhjdsklajfdslfjdsklfjkasljsa")

// 初始化输入系统
initInput(canvas);
// 启动游戏循环
gameLoop(performance.now());