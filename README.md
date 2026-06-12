# astrbot_plugin_random_pic

从指定目录中随机选取图片并发送的 AstrBot 插件。

## 功能

- 🔑 **关键字触发**：发送预设关键字即可触发（默认：随机图片）
- 📁 **自定义图片目录**：指定任意目录作为图库
- 🔢 **自定义发送数量**：每次随机发送 1~N 张图片
- 🔄 **递归搜索**：支持搜索子目录中的图片
- 🖼️ **多格式支持**：JPG、PNG、GIF、WebP、BMP
- 🖥️ **跨平台运行**：Windows / Linux / Docker 均可运行
- 📟 **命令触发**：同时支持 /randompic 命令

## 安装

### 方式一：AstrBot 插件市场（推荐）

在 AstrBot WebUI 的「插件市场」中搜索 strbot_plugin_random_pic，一键安装。

### 方式二：手动安装

`ash
# 进入 AstrBot 插件目录
cd AstrBot/plugins

# 克隆本仓库
git clone https://github.com/new-chara/astrbot_plugin_random_pic.git

# 重启 AstrBot
`

## 配置

在 AstrBot WebUI 的「插件配置」中找到「随机图片」插件，可配置以下选项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| keyword | string | 随机图片 | 触发关键字，发送该文字即可触发（留空则仅支持 /randompic 命令） |
| image_dir | string | ./random_pic | 图片存放目录，支持相对路径和绝对路径 |
| count | int | 1 | 每次发送的图片数量 |
| ecursive | bool | 	rue | 是否递归搜索子目录中的图片 |

### 路径说明

- **相对路径**：相对于 AstrBot 的运行目录（即启动 AstrBot 时所在的目录）
- **绝对路径**：
  - Windows：C:\Users\xxx\Pictures\random_pic
  - Linux/Docker：/data/images/random_pic

### Docker 挂载图片目录

如果使用 Docker 运行 AstrBot，建议将图片目录挂载到容器中：

`ash
docker run -d \
  -v /host/path/to/images:/data/images \
  ...其他参数...
  astrbot
`

然后在插件配置中将 image_dir 设置为 /data/images。

也可以直接将图片目录放在 AstrBot/data/ 下（该目录通常已挂载），然后使用相对路径如 ./data/random_pic。

## 使用

### 方式一：关键字触发

在聊天中直接发送配置的关键字（默认：随机图片）即可触发：

`
随机图片
`

→ 机器人将从指定目录随机选取图片发送。

### 方式二：命令触发

使用 /randompic 命令：

`
/randompic
`

> 命令方式始终可用，不受关键字配置影响。

## 支持的图片格式

- .jpg / .jpeg
- .png
- .gif
- .webp
- .bmp

大小写不敏感，即 .JPG 和 .jpg 均可识别。

## 项目结构

`
astrbot_plugin_random_pic/
├── metadata.yaml          # 插件元数据
├── main.py                # 插件主逻辑
├── _conf_schema.json      # 配置页面 schema
└── README.md              # 本文件
`

## 兼容性

- **AstrBot 版本**：>= 4.16, < 5
- **操作系统**：Windows / Linux / macOS
- **运行环境**：直接运行 / Docker 容器
- **消息平台**：所有 AstrBot 支持的平台（QQ、Telegram、Discord、微信、钉钉、飞书等）

## 常见问题

### Q: 发送「随机图片」后没反应？

1. 确认插件已在 WebUI 中启用
2. 检查 image_dir 路径是否正确，目录中是否有图片
3. 查看 AstrBot 日志中是否有 [RandomPic] 相关输出

### Q: 如何让多个关键字触发？

可以在 AstrBot 中安装多个本插件实例（复制插件目录并修改 metadata.yaml 中的 name），每个实例配置不同的关键字和图片目录。

### Q: Docker 中路径怎么配置？

使用容器内的路径。例如将宿主机 /home/user/pics 挂载到容器 /data/pics，则配置 image_dir 为 /data/pics。

## 许可证

MIT License
