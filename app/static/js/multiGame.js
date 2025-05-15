export class GameClient {
    constructor(canvas, roomId) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.roomId = roomId;
        this.playerId = null;
        this.players = new Map();
        this.bullets = new Set();

        // 初始化连接
        this.socket = new WebSocket(`ws://${location.host}/game/${roomId}/ws`);
        this.setupSocket();
        this.setupControls();
        this.gameLoop();
    }

    setupSocket() {
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            switch(data.type) {
                case 'init':
                    this.playerId = data.playerId;
                    Object.entries(data.players).forEach(([id, player]) => 
                        this.players.set(id, player)
                    );
                    break;
                    
                case 'playerUpdate':
                    if (this.players.has(data.playerId)) {
                        Object.assign(this.players.get(data.playerId), data);
                    }
                    break;
                    
                case 'bulletCreate':
                    this.bullets.add(data.bullet);
                    break;
                    
                case 'playerLeave':
                    this.players.delete(data.playerId);
                    break;
            }
        };
    }

    setupControls() {
        // 键盘控制
        const keyState = {};
        document.addEventListener('keydown', e => keyState[e.key] = true);
        document.addEventListener('keyup', e => keyState[e.key] = false);

        // 移动控制
        setInterval(() => {
            const speed = 8;
            let dx = 0, dy = 0;
            
            if (keyState['ArrowLeft']) dx = -speed;
            if (keyState['ArrowRight']) dx = speed;
            if (keyState['ArrowUp']) dy = -speed;
            if (keyState['ArrowDown']) dy = speed;

            if (dx || dy) {
                this.socket.send(JSON.stringify({
                    type: 'move',
                    dx, dy
                }));
            }
        }, 16);

        // 鼠标射击
        this.canvas.addEventListener('click', e => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.socket.send(JSON.stringify({
                type: 'fire',
                x: this.players.get(this.playerId)?.x || 400,
                y: this.players.get(this.playerId)?.y || 500,
                direction: { x, y }
            }));
        });
    }

    gameLoop() {
        // 渲染循环
        const render = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            // 渲染玩家
            this.players.forEach(player => {
                this.ctx.fillStyle = player.color;
                this.ctx.fillRect(player.x, player.y, 40, 40);
            });
            
            // 渲染子弹
            this.ctx.fillStyle = "#FF0000";
            this.bullets.forEach(bullet => {
                this.ctx.beginPath();
                this.ctx.arc(bullet.x, bullet.y, 3, 0, Math.PI * 2);
                this.ctx.fill();
            });
            
            requestAnimationFrame(render);
        };
        render();
    }
}

// 在 GameClient 类中添加以下方法
class GameClient {
  constructor(canvas, roomId) {
    // 初始化粒子池
    this.bulletParticles = new ParticlePool(1000);
    this.explosionPools = new Map(); // 每个玩家对应一个爆炸粒子池
  }

  // 炫酷子弹效果（能量光束+尾迹粒子）
  #createBulletEffect(x, y, angle) {
    // 主光束（渐变能量条）
    const gradient = this.ctx.createLinearGradient(x, y, x + Math.cos(angle)*30, y + Math.sin(angle)*30);
    gradient.addColorStop(0, 'rgba(255, 100, 0, 0.8)');
    gradient.addColorStop(1, 'rgba(255, 255, 0, 0.2)');

    // 尾迹粒子
    for(let i = 0; i < 5; i++) {
      this.bulletParticles.add({
        x, y,
        vx: Math.cos(angle) * 10 + Math.random()*2-1,
        vy: Math.sin(angle) * 10 + Math.random()*2-1,
        life: 0.8,
        color: `hsl(${Math.random()*30 + 30}, 100%, 50%)`
      });
    }

    return gradient;
  }

  // 空格键监听
  #setupControls() {
    document.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && Date.now() - this.lastFire > 100) { // 发射间隔100ms
        const bullet = this.player.fire();
        this.socket.emit('shoot', bullet); // 发送射击事件
        this.lastFire = Date.now();
      }
    });
  }
}

class GameClient {
  constructor() {
    this.players = new Map(); // 存储所有玩家对象
  }

  // 网络同步其他玩家
  #setupNetwork() {
    this.socket.on('playerJoin', (playerData) => {
      const fighter = new Fighter(playerData.x, playerData.y);
      fighter.id = playerData.id;
      this.players.set(playerData.id, fighter);
      this.explosionPools.set(playerData.id, new ParticlePool(500)); // 为每个玩家创建爆炸池
    });

    this.socket.on('playerShoot', (bullet) => {
      if (bullet.playerId !== this.player.id) {
        this.#createEnemyBulletEffect(bullet);
      }
    });
  }

  // 渲染所有战机（差异化样式）
  #renderPlayers() {
    this.players.forEach(player => {
      if (player.id === this.player.id) {
        this.#drawPlayerShip(player, '#00FF88'); // 己方绿色
      } else {
        this.#drawPlayerShip(player, '#FF3300'); // 敌方红色
        this.#renderEnemyHealthBar(player); // 显示敌方血条
      }
    });
  }
}


// 物理引擎扩展
class PhysicsEngine {
  static checkBulletHits(bullet, players) {
    for (const [id, player] of players) {
      if (this.circleCollision(
        bullet.x, bullet.y, 3,
        player.x, player.y, player.radius
      )) {
        return { hitPlayerId: id, bullet };
      }
    }
    return null;
  }
}

// 得分逻辑
class ScoreSystem {
  constructor() {
    this.score = 0;
    this.combo = 0;
    this.lastHitTime = 0;
  }

  addHit() {
    const timeDiff = Date.now() - this.lastHitTime;
    this.combo = timeDiff < 2000 ? this.combo + 1 : 1;
    this.score += 100 * this.combo;
    this.lastHitTime = Date.now();
  }

  render(ctx) {
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '20px Arial';
    ctx.fillText(`SCORE: ${this.score}   COMBO: x${this.combo}`, 10, 30);
  }
}

// 当检测到命中时
function handleHit(hitData) {
  const explosion = this.explosionPools.get(hitData.hitPlayerId);
  for(let i = 0; i < 50; i++) { // 爆炸碎片
    explosion.add({
      x: hitData.bullet.x,
      y: hitData.bullet.y,
      vx: Math.random() * 8 - 4,
      vy: Math.random() * 8 - 4,
      life: 1.5,
      color: `hsl(${Math.random()*60}, 100%, 50%)`
    });
  }

  // 屏幕震动
  this.camera.shake(10, 800);

  // 得分更新
  this.scoreSystem.addHit();
}