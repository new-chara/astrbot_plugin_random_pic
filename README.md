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
| image_dir | string | （留空） | 图片存放目录的绝对路径。留空则自动使用插件目录下的 random_pic 文件夹 |
| count | int | 1 | 每次发送的图片数量 |
| recursive | bool | true | 是否搜索子目录中的图片 |

> **修改配置后无需重启**，下次触发时自动生效。

## 使用教程

### 第一步：准备图片

插件安装后会自动包含一个 `random_pic` 文件夹，直接将图片放进去即可，无需额外配置路径。
如需使用其他目录，在配置中填写该目录的绝对路径。

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

如需使用其他目录，在 WebUI 中将 `image_dir` 设置为该目录的绝对路径。留空则自动使用插件自带的 `random_pic` 文件夹。

**绝对路径写法举例**：

- Windows：
  ```
  D:/images/my_pics
  ```
- Linux：
  ```
  /home/user/my_pics
  ```
- Docker 容器内：
  ```
  /data/images
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

Docker 容器内部和宿主机的文件系统是隔离的，图片目录必须通过 **挂载（volume mount）** 才能被插件访问到。以下是三种常用方案。

#### 方案一：挂载宿主机目录（推荐）

将宿主机上的图片目录挂载到容器内的一个固定路径，然后在插件配置中指向容器内路径。

**1. 启动容器时挂载目录：**

```bash
docker run -d \
  --name astrbot \
  -v /home/user/my_pics:/data/images \
  -v /home/user/astrbot_data:/AstrBot/data \
  astrbot_image
```

这里做了两个挂载：
- `/home/user/my_pics` → `/data/images`：你的图片目录
- `/home/user/astrbot_data` → `/AstrBot/data`：AstrBot 持久化数据目录（插件、配置等）

**2. 在插件配置中设置 `image_dir`：**

```
/data/images
```

**3. 将图片放到宿主机目录：**

```bash
# 在宿主机上执行
cp *.jpg /home/user/my_pics/
```

> 宿主机目录中新增的图片会实时反映到容器内，无需重启容器。

#### 方案二：使用插件自带的 random_pic 目录

插件安装后，其目录下已经包含一个空的 `random_pic/` 文件夹。这个文件夹在容器内的完整路径为：

```
/AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic
```

只要你已经挂载了 `/AstrBot/data` 目录（通常都会挂载用于持久化），就可以直接在宿主机上向这个目录放图片：

```bash
# 在宿主机上执行
# 路径取决于你挂载 /AstrBot/data 时对应的宿主机路径
cp *.jpg /home/user/astrbot_data/plugins/astrbot_plugin_random_pic/random_pic/
```

然后在插件配置中将 `image_dir` 设为以下容器内的绝对路径：

```
/AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic
```

#### 方案三：使用 docker cp 拷贝图片

如果不方便挂载目录，也可以用 `docker cp` 直接将图片拷贝到容器内：

```bash
# 拷贝单个文件
docker cp cat.jpg astrbot:/AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic/

# 拷贝整个目录
docker cp ./my_pics/. astrbot:/AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic/
```

> 注意：这种方式拷贝的图片在容器重建后会丢失，建议仅用于临时测试。

#### 验证挂载是否成功

进入容器检查图片目录是否可访问：

```bash
# 进入容器
docker exec -it astrbot bash

# 查看图片目录
ls -la /data/images
# 或
ls -la /AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic
```

确认目录存在且有图片文件后，在插件配置中填写相应的容器内路径即可。
