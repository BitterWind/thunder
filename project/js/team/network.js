import { CONFIG, entities, game_data } from './config.js';

// 角色初始数据请求方法，这个函数无法返回网络相关的参数，所以数据需要写入game_data
export async function get_id(name, mode, room=-1) {//player id , mode, room id,
    try {
        const response = await fetch(CONFIG.GET_ID, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "name":name,
                "mode":mode,
                "room":room
            })//string转换
        });
        // 这里的result不是一个正常的东西需要进行转换,而且await中的东西不能直接当参数传递，需要额外处理
        const result = await response.json();

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        game_data.team_member.id   = result.id
        if(mode>=3 ) game_data.team_member.name = result.name
        game_data.id    = result.id

        console.log('player_init :', game_data);
        
        return 1
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 角色初始数据请求方法，这个函数无法返回网络相关的参数，所以数据需要写入game_data
export async function get_room(name, mode, obj) {//player id , room id,
    try {
        const response = await fetch(CONFIG.GET_ROOM, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":name, "mode":mode, "obj":obj})//string转换
        });
        // 这里的result不是一个正常的东西需要进行转换,而且await中的东西不能直接当参数传递，需要额外处理
        const result = await response.json();
        // console.log('id_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        return 1
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 用来给创建房间的player更新房间数据，随时加入新玩家
export async function get_room_update(name, mode, obj) {//player id , room id,
    try {
        const response = await fetch(CONFIG.GET_ROOM_UPDATE, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":name, "mode":mode, "obj":obj})//string转换
        });
        // 这里的result不是一个正常的东西需要进行转换,而且await中的东西不能直接当参数传递，需要额外处理
        const result = await response.json();
        // console.log('id_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        game_data.team_member.id   = result.id+1 
        game_data.team_member.name = mode=
        console.log('lobby get data :', game_data);

        return 1
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

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
export async function data_send(player_data) {
    console.log('data_send Response:', entities.players);
    try {
        const response = await fetch(CONFIG.SEND_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(player_data)//string转换
        });
        // if(game_data.time_cnt==60)console.log('data_send Response:', player_data);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    } catch (error) {
        console.error('发送失败:', player_data ,error);
    }
}

// 数据请求方法
export async function data_request() {
    try {
        const response = await fetch(CONFIG.GET_DATA, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"name":game_data.team_member.name, "id":game_data.team_member.id, "mode":game_data.mode})//string转换
        });
        // console.warn('乱七八糟MouseMove', e);
        const result = await response.json();
        console.log('data_request players :', entities.players);
        entities.players[1].position=result.position;

        // if(game_data.time_cnt==60)console.log('data_request return:', entities.players[1]);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // console.warn('请求返回:', response);
        return result
    } catch (error) {
        console.error('请求失败:', team_member ,error);
    }
}

