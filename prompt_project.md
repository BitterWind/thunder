---
marp: true
theme: default
paginate: true
header: "雷霆战机全栈项目"
style: |
    section {
        background-color: rgb(239, 232, 232);
        color: rgb(22, 22, 22);
        font-family: Arial, sans-serif;
        padding: 20px;
    }
    h1, h2, h3 {
        color: rgb(96, 120, 105);
    }
    ul {
        margin-left: 20px;
    }
    li {
        line-height: 1.6;
    }
---
<!-- 这个很有用 -->
<style>
section::after {
  content: attr(data-marpit-pagination) '/' attr(data-marpit-pagination-total);
}
</style>
# 雷霆战机全栈项目

这是一个模仿雷霆战机的全栈项目，包含以下技术栈：

---

## 前端

- **技术栈**: 原生 JavaScript、CSS、HTML
- **功能**: 
    - 实现游戏界面。
    - 支持用户交互和动画效果。

---

## 网络层

- **技术栈**: 原生组件和 WebSocket
- **功能**: 
    - 实现实时通信。
    - 支持多人在线对战。

---

## 后端

- **框架**: FastAPI
- **功能**: 
    - 提供游戏逻辑处理。
    - 实现用户管理和 API 接口。

---

## 数据库

- **Redis**: 
    - 用于缓存和实时数据存储。
- **SQLite**: 
    - 用于持久化存储用户数据和游戏记录。

---

## 项目特点

- 全栈开发，涵盖前端、后端和数据库。
- 实现实时通信和高效数据处理。
- 模仿经典游戏雷霆战机，提供完整的游戏体验。

---

## 运行方式

1. 启动后端服务（FastAPI）。
2. 启动前端页面，连接后端。
3. 开始游戏，体验雷霆战机的乐趣！
