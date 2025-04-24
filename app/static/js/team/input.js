import { entities, game_data } from './config.js';
import { leave_room } from './network.js';
export function initInput(canvas) {

    // 输入监听系统，只更新主玩家的数据内容，双人模式下的副玩家通过data_request()更新
    window.addEventListener('keydown', e => onKeyDown(e));
    window.addEventListener('keyup', e => onKeyUp(e));
    // 页面关闭处理， 妈的，人类的时代已经结束了。
    window.addEventListener('beforeunload', () => {
        leave_room();
    });
    canvas.addEventListener('mousedown', e => {
        entities.players[0].keyMouse.Mouse = true;
        entities.players[0].mouse.x=e.clientX;
        entities.players[0].mouse.y=e.clientY;
    });
    canvas.addEventListener('mouseup', e => {
        // console.log('乱七八糟MouseUp', e);
        entities.players[0].keyMouse.Mouse = false;
    });
    canvas.addEventListener('mousemove', e => {//这是个类似于 lambda的简单内嵌函数。
        // console.log('乱七八糟MouseMove', entities.players[0]);
        entities.players[0].mouse.x=e.clientX;
        entities.players[0].mouse.y=e.clientY;
    });
}

//键盘事件检测
export function onKeyDown(e){
    // if (e.code === 'Enter') entities.players[0].keys.Enter = true;
    if (e.code === 'KeyA') entities.players[0].keyMouse.KeyA = true;
    if (e.code === 'KeyD') entities.players[0].keyMouse.KeyD = true;
    if (e.code === 'KeyW') entities.players[0].keyMouse.KeyW = true;
    if (e.code === 'KeyS') entities.players[0].keyMouse.KeyS = true;
}
export function onKeyUp(e){
    // if (e.code === 'Enter') entities.players[0].keys.Enter = false;
    if (e.code === 'KeyA') entities.players[0].keyMouse.KeyA = false;
    if (e.code === 'KeyD') entities.players[0].keyMouse.KeyD = false;
    if (e.code === 'KeyW') entities.players[0].keyMouse.KeyW = false;
    if (e.code === 'KeyS') entities.players[0].keyMouse.KeyS = false;
}

export function init() {
    // 添加双重空值检查
    const storageData = sessionStorage.getItem('game_data');

    if (!storageData || storageData === "null") {
        // 生成4人默认数据
        game_data = {
            players: Array(4).fill().map((_,i) => ({
                id: i+1,
                ready: false
            }))
        };
        console.error('致命错误：缺失游戏数据');
        sessionStorage.removeItem('game_data');
        //window.location.href = 'lobby.html';
        return;
    }

    try {
        const parsedData = JSON.parse(storageData);

        // 深度合并对象（增强版）
        game_data = {
            ...game_data,     // 保留默认值
            ...parsedData,    // 应用存储值
            team_member: {    // 处理嵌套属性
                ...game_data.team_member,
                ...parsedData.team_member
            }
        };
    } catch (error) {
        console.error('数据解析失败:', error);
        sessionStorage.clear();
        window.location.reload();
    }
}
// "{\"game_data\":{\"room\":1,\"mode\":1,\"name\":\"default_name\",\"id\":2,\"team_member\":{\"name\":\"default_name\",\"id\":1},\"ready\":1}}"