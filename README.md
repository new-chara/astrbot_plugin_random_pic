# astrbot_plugin_random_pic

从指定目录中随机选取图片并发送的 AstrBot 插件。

## 功能

- 发送任意一个预设关键字即可触发，从指定目录随机发送图片
- 支持配置多个触发关键字（每行一个）
- 支持自定义图片目录、发送数量
- 支持 /randompic 命令触发
- 支持递归搜索子目录
- 支持 jpg / png / gif / webp / bmp 格式

## 配置

在 AstrBot WebUI 中，进入「插件配置」页，找到「随机图片」插件进行配置。

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| keywords | text | 随机图片 | 触发关键字，每行一个。发送任意一个即可触发。留空则仅支持 /randompic 命令 |
| image_dir | string | ./random_pic | 图片存放目录，支持相对路径和绝对路径 |
| count | int | 1 | 每次发送的图片数量 |
| recursive | bool | true | 是否搜索子目录中的图片 |

> **修改配置后无需重启**，下次触发时自动生效。

## 使用教程

### 第一步：准备图片

插件安装后，会自动包含一个 `random_pic` 文件夹，你可以直接将图片放进去。
也可以在配置中将 `image_dir` 改为其他目录。

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

在 WebUI 中配置 `image_dir` 指向你的图片目录。默认为插件目录下的 `random_pic` 文件夹。

**其他路径写法举例**：

- 图片放在 AstrBot 目录下：
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

在 WebUI 中设置 `keywords`，每行一个关键字，例如：

```
随机图片
来点图
看看图
```

发送其中任意一个即可触发。

> 留空则表示不启用关键字触发，只能通过 `/randompic` 命令触发。

### 第四步：设置发送数量

`count` 控制每次触发时发送的图片数量。设为 1 则每次发 1 张，设为 3 则每次随机发 3 张（不重复）。

### 第五步：开始使用

在聊天中发送你设置的任意一个关键字，或发送 `/randompic` 命令，即可收到随机图片。

### Docker 环境使用

如果用 Docker 运行 AstrBot，需要使用 `-v` 参数将图片目录挂载进容器：

```bash
docker run -d \
  -v /home/user/my_pics:/data/images \
  astrbot_image
```

然后在插件配置中将 `image_dir` 设为容器内的路径 `/data/images`。

也可以在 `AstrBot/data/` 目录下创建文件夹存放图片（该目录通常已经挂载），然后配置相对路径如 `./data/my_pics`。
