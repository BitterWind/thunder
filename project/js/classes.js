//类的实现。
import { CONFIG, entities , game_state, canvas, ctx } from './config.js';

//position
export class Vector2 {
    constructor(x=0, y=0) {
        this.x = x;
        this.y = y;
    }
    normalize() {
        const length = Math.sqrt(this.x**2 + this.y**2);
        return new Vector2(this.x/length, this.y/length);
    }  
}

//键盘状态
export class KeyMouse {
    constructor(a,s,w,d,m) {
        this.KeyA = a;
        this.KeyS = s;
        this.KeyW = w;
        this.KeyD = d;
        this.Mouse = m;
    }
}

//所有的游戏逻辑实体
export class GameObject {
    //基础数据
    constructor(position, size, color) {
        this.position = position;
        this.size = size;
        this.color = color;
        this.active = true;
    }

    //绘制，后面把图标替换一下
    draw() {
        if(this.active){
            ctx.fillStyle = this.color;
            ctx.fillRect(
                this.position.x - this.size/2,
                this.position.y - this.size/2,
                this.size,
                this.size
            );
        }
    }

}

//游戏逻辑实体 ： 玩家
export class Player extends GameObject {
    //新增数据，包括所有的键盘状态，每个玩家都有自己的一套键盘状态。
    constructor(dic) {
        super(new Vector2(canvas.width/2, canvas.height-50), CONFIG.PLAYER_SIZE, `hsl(${Math.random()*360}, 70%, 60%)`);//继承的
        this.speed = CONFIG.PLAYER_SPEED;//速度
        this.keyMouse=new KeyMouse(false,false,false,false,false);//player对应单独键盘监听系统
        this.mouse=new Vector2(0,0);
        this.id=dic["name"]; 
        this.room=dic["room"]; 
        this.name=game_state.name;//后面需要让name在图标的头顶标记着。
        this.shooterCnt=0;//双人模式下用来实时同步血量，对的这里的护卫机也是血量的表现。
    }

    update(deltaTime){
        if (this.keyMouse.KeyA) this.position.x -= this.speed * deltaTime;
        if (this.keyMouse.KeyD) this.position.x += this.speed * deltaTime;
        if (this.keyMouse.KeyW) this.position.y -= this.speed * deltaTime;
        if (this.keyMouse.KeyS ) this.position.y += this.speed * deltaTime;

        this.position.x = Math.max(CONFIG.PLAYER_SIZE/2, Math.min(canvas.width-CONFIG.PLAYER_SIZE/2, this.position.x));//限制位置不超过左右边界
        this.position.y = Math.max(CONFIG.PLAYER_SIZE/2, Math.min(canvas.height-CONFIG.PLAYER_SIZE/2, this.position.y));//上下边界
        // // 结构化日志输出
        // if(game_state.timeCnt==60)console.log('%c核心状态:', 'color: #2ecc71; font-weight: bold', {
        //     position: `(${this.position.x}, ${this.position.y})`,
        //     velocity: `px/frame`
        // });浏览器inspect居然有控制台？！
    }

    //发射子弹，
    fire(){
        const rect = canvas.getBoundingClientRect();
        //当前object到鼠标的方向向量
        const direction = new Vector2(
            (this.mouse.x  - rect.left) -this.position.x,
            (this.mouse.y  - rect.top) - this.position.y
        );
        entities.bullets.push(new Bullet(
            new Vector2(this.position.x, this.position.y),
            direction
        ));
    }
}

//游戏逻辑实体 ： 子弹
export class Bullet extends GameObject {
    constructor(position,direction) {
        super(new Vector2(position.x,position.y),
            CONFIG.BULLET_SIZE,
            `hsl(${Math.random()*360}, 70%, 60%)`
        );
        this.speed = CONFIG.BULLET_SPEED + Math.random()*CONFIG.BULLET_SPEED;
        this.direction=direction.normalize();
        this.trail=[]; // 弹道轨迹缓存，可以制造拖尾效果
    }

    update(deltaTime) {
        this.position.x += this.direction.x * this.speed;
        this.position.y += this.direction.y * this.speed;
        this.trail.push({...this.position});
        if(this.trail.length > 10) this.trail.shift();
        if(this.active)this.active = ( this.position.y > -10 );
    }
}

//游戏逻辑实体 ： 敌机
export class Enemy extends GameObject {
    constructor() {
        super(
            new Vector2(Math.random()*(canvas.width-40)+20, -30),
            25,
            `hsl(${Math.random()*360}, 70%, 60%)`
        );
        this.speed = 200 + Math.random()*100;
    }

    update(deltaTime) {
        this.position.y += this.speed * deltaTime;
        if(this.active) this.active = ( this.position.y < canvas.height + 20 );
    }
    fire2(){//还没做好
    }
}

//游戏逻辑实体 ： 护卫机
export class Shooter extends GameObject {
    constructor(PlayerNumber) {
        super(
            new Vector2(0,0),
            25,
            `hsl(${Math.random()*360}, 70%, 60%)`
        );
        this.belong = PlayerNumber;
        this.angle = 0.00;//弧度
    }

    update(deltaTime) {
        this.position.x = entities.players[this.belong].position.x + CONFIG.SHOOTER_RIDUS * Math.cos(this.angle);
        this.position.y = entities.players[this.belong].position.y + CONFIG.SHOOTER_RIDUS * Math.sin(this.angle);
        this.angle += CONFIG.SHOOTER_SPEED/60;//弧度
        if(this.active) this.active = entities.players[this.belong].active;
    }

    //子弹发射与player同步。
    fire(){
        const rect = canvas.getBoundingClientRect();
        const direction = new Vector2(//当前object到鼠标的方向向量
            (entities.players[this.belong].mouse.x - rect.left) - this.position.x,
            (entities.players[this.belong].mouse.y - rect.top ) - this.position.y
        );
        entities.bullets.push(new Bullet(
            new Vector2(this.position.x, this.position.y),
            direction
        ));
    }
}