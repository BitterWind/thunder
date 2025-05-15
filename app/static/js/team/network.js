import { CONFIG, entities, game_data } from './config.js';

// 角色初始数据发送方法，
export async function send_score(score) {
    // console.log('发送请求 :', typeof(JSON.stringify(team_member)));#可以优化的内容很多很多。
    try {
        console.log('score send:', JSON.stringify({"id":game_data.id, "score":score}));
        const response = await fetch(CONFIG.SEND_SCORE, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"id":game_data.id, "score":score})//string转换
        });
        const result = await response.json();
        console.log('score return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return result["rank"]
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 排行榜数据请求方法，
export async function leaderboard_request() {//id , room ,
    // console.warn('发送请求 :', typeof(JSON.stringify(team_member)));#可以优化的内容很多很多。
    try {
        const response = await fetch(CONFIG.GET_LEADERBOARD, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"id":game_data.id})//string转换
        });
        const result = await response.json();
        console.log('leaderboard_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return 0
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 数据发送方法
// network.js
export async function data_send(data) {
    try {
        console.log('data_send :', data);
        const response = await fetch(CONFIG.SEND_DATA, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: data.id,
                position: data.position,
                keyMouse: data.keyMouse,
                mouse: data.mouse
            })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

export async function data_request() {
    try {
        const response = await fetch(CONFIG.GET_DATA, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: game_data.id }) // 确保使用正确的 player_id
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail}`);
        }
        const result = await response.json();
        console.log('data of players request:', result);
        if (result && result.mouse) {
            console.log('Mouse now of player 1', result.mouse);
            entities.players[1].position = result.position;
            entities.players[1].keyMouse = result.keyMouse;
            entities.players[1].mouse = result.mouse;
        } else {
            console.error('请求返回的数据格式不正确');
        }
        return result;
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 离开房间，清除房间数据，在窗口调整或者关闭时调用
export async function leave_room() {//player id , room id,
    const response = await fetch(CONFIG.LEAVE_ROOM, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"id":game_data.id, "room":game_data.room})//string转换
    });
    const result = await response.json();
    console.log('leave room return:', result);
    if (result.success) {
        sessionStorage.clear();
        window.location.href = `lobby.html`;
    }
    return 1
}