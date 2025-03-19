import { entities, canvas, game_state} from './config.js';
import { initInput } from './input.js';
import { gameLoop } from './gameLogic.js';
import { Player } from './classes.js';
import { player_init } from './network.js';

// 初始化玩家和房间等环境配置数据，这里还需要一些参数，例如房间名称，因为从逻辑上来说，是先创建房间，再来到这个游戏界面的。
// 现在由于登录逻辑还有需要补充的部分，这里先放放 TO_DO
player_init();

entities.players.push(new Player());
// entities.players.push(new Player(1));
// document.write("fhjdsklajfdslfjdsklfjkasljsa")

// 初始化输入系统
initInput(canvas);
// 启动游戏循环
gameLoop(performance.now());