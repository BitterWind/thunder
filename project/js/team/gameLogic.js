import { entities, CONFIG, canvas, ctx, game_data } from './config.js';
import { Enemy, Shooter} from './classes.js';
import { send_score, data_send, data_request} from './network.js';

export let lastFrameTime = 0;
export let lastFireTime = 0;
export let lastAddTime = 0;

//更新游戏实体  
export function updateEntities(list, deltaTime) {
    for (let i = list.length-1; i >= 0; i--) {
        list[i].update(deltaTime);
        if (!list[i].active) list.splice(i, 1);
    }
}

//子弹与敌机的碰撞检测，后续追加子弹与护卫机的，玩家不会死，也不会挡子弹。
export function checkCollisions() {
    // 使用优化后的检测方法
    for(let i = entities.enemies.length-1; i >=0; i--){
        for(let j = entities.bullets.length-1; j >=0; j--){
            const dx = entities.enemies[i].position.x - entities.bullets[j].position.x;
            const dy = entities.enemies[i].position.y - entities.bullets[j].position.y;
            // const dy = enemy.position.y - bullet.position.y;
            if (dx*dx + dy*dy < Math.pow(( entities.enemies[i].size +  entities.bullets[j].size)/2, 2) && entities.bullets[j].active) {
                entities.enemies[i].active =  false;
                entities.bullets[j].active = false;
                game_data.score+=1;
            }
        }
    }
}

// 游戏循环
export function gameLoop(timestamp) {
    const deltaTime = (timestamp - lastFrameTime) / 1000;
    lastFrameTime = timestamp;

    // 清除画布
    ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
    ctx.fillRect(0, 0, canvas.width, canvas.height); 
    

    // 发射子弹
    if (timestamp - lastFireTime > CONFIG.FIRE_RATE){//实际上，这里的频率最高也就是电脑屏幕的60hz，硬件限制，而不是算力受限。
        if(entities.players[0].keyMouse.Mouse){
            entities.players[0].fire();
            entities.shooters1.forEach(s => s.fire());
        }
        if (entities.players[1].keyMouse.Mouse){ //&&fire
            entities.players[1].fire();
            entities.shooters2.forEach(s => s.fire());
        }
        lastFireTime = timestamp;
    }
    // 增加shooter
    if ( timestamp - lastAddTime > CONFIG.ADD_SHOOTER_RATE){//实际上，这里的频率最高也就是电脑屏幕的60hz，硬件限制，而不是算力受限。
        lastAddTime = timestamp;
        if(entities.players[0].shooter_cnt <= CONFIG.SHOOTER_LIMIT ){
            entities.shooters1.push(new Shooter(0));//接下来要加个玩家。
            entities.players[0].shooter_cnt++;
        }
        if(entities.players[1].shooter_cnt <= CONFIG.SHOOTER_LIMIT ){
            entities.shooters2.push(new Shooter(1));//接下来要加个玩家。
            entities.players[1].shooter_cnt++;
        }
    }
    // 更新实体
    updateEntities(entities.bullets, deltaTime);
    updateEntities(entities.enemies, deltaTime);
    updateEntities(entities.players, deltaTime);
    updateEntities(entities.shooters1, deltaTime);
    updateEntities(entities.shooters2, deltaTime);

    // 生成敌人
    if (Math.random() < CONFIG.ENEMY_SPAWN_RATE) {
        entities.enemies.push(new Enemy());
    }

    // 碰撞检测
    checkCollisions();

    // 渲染
    entities.players.forEach(p => p.draw());
    entities.bullets.forEach(b => b.draw());
    entities.enemies.forEach(e => e.draw());
    entities.shooters1.forEach(s => s.draw());
    entities.shooters2.forEach(s => s.draw());
    // data_send(entities.players[0]);
    // data_request();
    game_data.time_cnt++;
    if(game_data.time_cnt==122){
        game_data.time_cnt=0;
        // update_leader_board();
        send_score(game_data.score);
        data_send(entities.players[0]);
        data_request();
        // leaderboard_request();
        console.log('user data', game_data);
    }
    requestAnimationFrame(gameLoop);//在此调用自身，并将时间作为参数回传
}
