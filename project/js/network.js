import { CONFIG, entities } from './config.js';

// 数据发送方法
export async function dataSend(player_data) {
    console.log('dataSend Response:', entities.players);
    try {
        const response = await fetch(CONFIG.SEND_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(player_data)//string转换
        });
        // if(gameState.timeCnt==60)console.log('dataSend Response:', player_data);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    } catch (error) {
        console.error('发送失败:', player_data ,error);
    }
}

// 数据请求方法
export async function dataRequest() {
    // console.warn('发送请求 :', typeof(JSON.stringify(TeamMember)));
    try {
        const response = await fetch(CONFIG.GET_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":TeamMember,"mode":Mode})//string转换
        });
    // console.warn('乱七八糟MouseMove', e);
        const result = await response.json();
        console.log('dataRequest players :', entities.player);
        entities.players[1].position=result.position;
        // if(gameState.timeCnt==60)console.log('dataRequest return:', entities.players[1]);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // console.warn('请求返回:', response);
        return result
    } catch (error) {
        console.error('请求失败:', TeamMember ,error);
    }
}

// 数据请求方法
export async function idRequest() {
    // console.warn('发送请求 :', typeof(JSON.stringify(TeamMember)));
    try {
        const response = await fetch(CONFIG.GET_ID, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":TeamMember,"mode":Mode})//string转换
        });
    // console.warn('乱七八糟MouseMove', e);
        const result = await response.json();
        console.log('dataRequest players :', entities.player);
        entities.players[1].position=result.position;
        // if(gameState.timeCnt==60)console.log('dataRequest return:', entities.players[1]);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // console.warn('请求返回:', response);
        return result
    } catch (error) {
        console.error('请求失败:', TeamMember ,error);
    }
}