import { CONFIG, game_data } from './config.js';

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

