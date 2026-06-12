# astrbot_plugin_random_pic

从指定目录中随机选取图片并发送的 AstrBot 插件。

## 功能

- 发送预设关键字触发插件，从指定目录随机发送图片
- 支持自定义触发关键字、图片目录、发送数量
- 支持 /randompic 命令触发
- 支持递归搜索子目录
- 支持 jpg / png / gif / webp / bmp 格式

## 安装

### 方式一：插件市场安装

在 AstrBot WebUI 的「插件市场」中搜索 `astrbot_plugin_random_pic` 并安装。

### 方式二：手动安装

```bash
# 进入 AstrBot 插件目录
cd AstrBot/plugins

# 克隆本仓库
git clone https://github.com/new-chara/astrbot_plugin_random_pic.git

# 重启 AstrBot
```

## 配置

在 AstrBot WebUI 中，进入「插件配置」页，找到「随机图片」插件进行配置。

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| keyword | string | 随机图片 | 触发关键字，在聊天中发送该文字即可触发。留空则仅支持 /randompic 命令 |
| image_dir | string | ./random_pic | 图片存放目录，支持相对路径和绝对路径 |
| count | int | 1 | 每次发送的图片数量 |
| recursive | bool | true | 是否搜索子目录中的图片 |

> **修改配置后无需重启**，下次触发时自动生效。

## 使用教程

### 第一步：准备图片

在 AstrBot 所在的机器上创建一个目录，将图片放进去。

**支持的图片格式**：`.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp`（不区分大小写）

**目录结构示例**：

```
random_pic/
├── cat.jpg
├── dog.png
├── memes/
│   ├── meme1.gif
│   └── meme2.webp
└── photos/
    └── sunset.jpg
```

### 第二步：配置图片目录

在 WebUI 中配置 `image_dir` 指向你的图片目录。

**路径写法举例**：

- 图片放在 AstrBot 目录下的 `random_pic` 文件夹中：
  ```
  ./random_pic
  ```
- Windows 下图片在 D 盘：
  ```
  D:/images/my_pics
  ```
- Linux / Docker 下图片在 `/data/pics`：
  ```
  /data/pics
  ```

### 第三步：配置触发关键字

在 WebUI 中将 `keyword` 设置为你想要的关键字，例如 `来点图`、`随机图片` 等。

> 留空则表示不启用关键字触发，只能通过 `/randompic` 命令触发。

### 第四步：设置发送数量

`count` 控制每次触发时发送的图片数量。设为 1 则每次发 1 张，设为 3 则每次随机发 3 张（不重复）。

### 第五步：开始使用

在聊天中发送你设置的关键字，或发送 `/randompic` 命令，即可收到随机图片。

### Docker 环境使用

如果用 Docker 运行 AstrBot，需要使用 `-v` 参数将图片目录挂载进容器：

```bash
docker run -d \
  -v /home/user/my_pics:/data/images \
  astrbot_image
```

然后在插件配置中将 `image_dir` 设为容器内的路径 `/data/images`。

也可以在 `AstrBot/data/` 目录下创建文件夹存放图片（该目录通常已经挂载），然后配置相对路径如 `./data/my_pics`。

## 常见问题

**Q: 发送关键字后没有反应？**

1. 确认插件已在 WebUI 中「启用」
2. 检查 `image_dir` 路径是否正确，目录是否存在
3. 检查目录中是否有 `.jpg` `.png` `.gif` `.webp` `.bmp` 格式的图片
4. 查看 AstrBot 日志，搜索 `[RandomPic]` 查看错误信息

**Q: 如何同时使用多个图库？**

复制插件目录，修改副本中 `metadata.yaml` 的 `name` 字段（不能重复），然后分别为每个实例配置不同的 `keyword` 和 `image_dir`。

**Q: 可以一次触发发多张不同的图吗？**

可以，将 `count` 设为你想要的数量即可，图片不会重复。

## 项目结构

```
astrbot_plugin_random_pic/
├── metadata.yaml          # 插件元数据
├── main.py                # 插件主逻辑
├── _conf_schema.json      # 配置页面描述
└── README.md              # 本文件
```

## 许可证

MIT License
