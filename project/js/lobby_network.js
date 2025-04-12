import { CONFIG, game_data } from './lobby_config.js';

// 角色初始数据请求方法，这个函数无法返回网络相关的参数，所以数据需要写入game_data
export async function get_id(name, mode, room=-1) {//player id , mode, 指定房间加入时对方的id room id,
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
        
        if (result.room==-1){
            alert('当前没有空闲的房间，请创建空房间。');
            return 0;
        }//房间不存在，返回0
        console.log('get_id return:', result);
        
        if(mode>=3 ){//一定有队友数据的模式
            game_data.team_member.id   = result.room;
            game_data.team_member.name = result.name;
        }
        game_data.id = result.id;
        game_data.room  = result.room;
        game_data.mode  = mode;
        game_data.name  = name;
        sessionStorage.setItem('game_data', JSON.stringify({game_data})); //这是个异步函数，时间上需要放到同一个函数中，保证异步运行单线程程序，否则时间上的数据结构会混乱。
        switch (mode) {
            case 2: sessionStorage.setItem('is_host',true); break;//创建房间
            case 3: sessionStorage.setItem('is_host',false); break;//随机匹配
            case 4: sessionStorage.setItem('is_host',false); break;//定向匹配
            default: console.error('未知的模式:', mode); 
        }
        if(mode==1) window.location.href = `index_single.html`//单人模式
        if(mode>=2) window.location.href = `waiting.html`
        
        return 1;

    } catch (error) {
        console.error('请求失败:' ,error);
        return 0;
    }
}

// 用来给创建房间的player更新房间数据，随时加入新玩家
export async function get_room_update(id, room) {//player id , room id,
    try {
        const response = await fetch(CONFIG.GET_ROOM_UPDATE, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"id":id, "room":room})//string转换
        });
        const result = await response.json();
        // console.log('id_request return:', result);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        console.log('get_room_update return:', result);
        if(result.ready==0) return 0;//队友不存在，返回0
        if(result.ready==1) {
            game_data.team_member.id   = result.id;
            game_data.team_member.name = result.name;
            game_data.ready            = 1;
            console.log('lobby get data :', game_data);
            return 1;
        }
    } catch (error) {
        console.error('请求失败:' ,error);
        return 0 ;
    }
}

// 用来给创建房间的player更新房间数据，随时加入新玩家
export async function leave_room(name, mode, obj) {//player id , room id,
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
        
        console.log('lobby get data :', game_data);
        sessionStorage.setItem('game_data',game_data);
        return 1
    } catch (error) {
        console.error('请求失败:' ,error);
    }
}

// 用来给创建房间的player更新房间数据，随时加入新玩家
export async function start_game(name, mode, obj) {//player id , room id,
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
