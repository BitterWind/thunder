import { CONFIG, entities, game_state } from './config.js';

// 数据发送方法
export async function data_send(player_data) {
    console.log('data_send Response:', entities.players);
    try {
        const response = await fetch(CONFIG.SEND_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(player_data)//string转换
        });
        // if(game_state.time_cnt==60)console.log('data_send Response:', player_data);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    } catch (error) {
        console.error('发送失败:', player_data ,error);
    }
}

// 数据请求方法
export async function data_request() {
    // console.warn('发送请求 :', typeof(JSON.stringify(team_member)));
    try {
        const response = await fetch(CONFIG.GET_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":team_member,"mode":Mode})//string转换
        });
    // console.warn('乱七八糟MouseMove', e);
        const result = await response.json();
        console.log('data_request players :', entities.player);
        entities.players[1].position=result.position;
        // if(game_state.time_cnt==60)console.log('data_request return:', entities.players[1]);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // console.warn('请求返回:', response);
        return result
    } catch (error) {
        console.error('请求失败:', team_member ,error);
    }
}

// 角色初始数据请求方法，
export async function player_init() {//id , room ,
    // console.warn('发送请求 :', typeof(JSON.stringify(team_member)));#可以优化的内容很多很多。
    try {
        const response = await fetch(CONFIG.GET_ID, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":"guy", "mode":1, "obj":0})//string转换
        });
        // 这里的result不是一个正常的东西需要进行转换
        const result = await response.json();
        // console.log('id_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        game_state.room = result.room
        game_state.id = result.id
        console.log('id_request return:', game_state);

        return result.id
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 角色初始数据请求方法，
export async function send_score(score) {//id , room ,
    // console.warn('发送请求 :', typeof(JSON.stringify(team_member)));#可以优化的内容很多很多。
    try {
        console.log('score send:', JSON.stringify({"id":game_state.id, "score":score}));
        const response = await fetch(CONFIG.SEND_SCORE, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"id":game_state.id, "score":score})//string转换
        });
        const result = await response.json();
        console.log('id_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return result["rank"]
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}