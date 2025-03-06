import { entities, CONFIG, canvas, ctx, gameState } from './config.js';
import { Enemy, Shooter} from './classes.js';

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
                // console.warn('敌人超出边界', entities.enemies[i])
                entities.bullets[j].active = false;
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
    
    //只有在双人模式的时候需要传送数据
    if(gameState.mode ==2 ){//&& Bool
        dataSend(entities.players[0]);
        dataRequest();
        // Bool=!Bool;
    }
    // 发射子弹
    if (timestamp - lastFireTime > CONFIG.FIRE_RATE){//实际上，这里的频率最高也就是电脑屏幕的60hz，硬件限制，而不是算力受限。
        if(entities.players[0].keyMouse.Mouse){
            entities.players[0].fire();
            entities.Shooters1.forEach(s => s.fire());
        }
        if(gameState.mode==2){
            if (entities.players[1].keyMouse.Mouse){ //&&fire
                entities.players[1].fire();
                entities.Shooters2.forEach(s => s.fire());
            }
        }
        lastFireTime = timestamp;
    }
    // 增加shooter
    if ( timestamp - lastAddTime > CONFIG.ADD_SHOOTER_RATE){//实际上，这里的频率最高也就是电脑屏幕的60hz，硬件限制，而不是算力受限。
        lastAddTime = timestamp;
        if(entities.players[0].shooterCnt <= CONFIG.SHOOTER_LIMIT ){
            entities.Shooters1.push(new Shooter(0));//接下来要加个玩家。
            entities.players[0].shooterCnt++;
        }
        if(gameState.mode==2 ){
            if(entities.players[1].shooterCnt <= CONFIG.SHOOTER_LIMIT ){
                entities.Shooters2.push(new Shooter(1));//接下来要加个玩家。
                entities.players[1].shooterCnt++;
            }
        }
    }
    // 更新实体
    updateEntities(entities.bullets, deltaTime);
    updateEntities(entities.enemies, deltaTime);
    updateEntities(entities.players, deltaTime);
    updateEntities(entities.Shooters1, deltaTime);
    if(gameState.mode==2)updateEntities(entities.Shooters2, deltaTime);

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
    entities.Shooters1.forEach(s => s.draw());
    if(gameState.mode==2)entities.Shooters2.forEach(s => s.draw());
    gameState.timeCnt++;
    if(gameState.timeCnt==61){
        gameState.timeCnt=0;
        console.log('user data', entities.players);
    }
    requestAnimationFrame(gameLoop);//在此调用自身，并将时间作为参数回传
}
