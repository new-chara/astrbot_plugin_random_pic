# astrbot_plugin_random_pic

AstrBot 随机图片插件 —— 发送指令后从本地目录随机返回图片。

## 功能

- 支持多个触发命令（如 `/randompic`、`/来张图`、`/随机图片`）
- 支持指定数量参数（如 `/randompic 2`，最多 3 张）
- 图片存放在本地任意目录，默认指向桌面
- 所有配置项可在 AstrBot Web 面板中直接修改，无需编辑文件

## 支持的图片格式

`.jpg` `.jpeg` `.png` `.gif` `.bmp` `.webp`

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `pics_dir` | string | 桌面路径 | 图片存放的文件夹绝对路径 |
| `triggers` | list | `["randompic", "来张图", "随机图片"]` | 触发命令列表 |
| `max_count` | int | `3` | 每次最多发送图片数量 |

## 使用

1. 将图片放入 `pics_dir` 指定的目录
2. 在聊天中发送触发命令，如 `/randompic` 或 `/随机图片 2`
3. Bot 将从目录中随机选取图片发送

## 链接

- [AstrBot](https://github.com/AstrBotDevs/AstrBot)
- [插件开发文档](https://docs.astrbot.app/dev/star/plugin-new.html)
