import os
import random
from pathlib import Path

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event.filter import EventMessageType
from astrbot.api.star import Context, Star
from astrbot.api import logger

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


class RandomPicPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # ─────────────────────────────
    # config 安全获取（关键修复点）
    # ─────────────────────────────
    async def _get_config(self) -> dict:
        try:
            config = await self.context.get_config()
        except Exception:
            config = {}

        if not isinstance(config, dict):
            config = {}

        raw = config.get("keywords", config.get("keyword", "随机图片"))

        if isinstance(raw, str):
            keywords = [k.strip() for k in raw.split("\n") if k.strip()]
        else:
            keywords = list(raw) if raw else []

        image_dir = config.get("image_dir")

        return {
            "keywords": keywords,
            "image_dir": image_dir,   # ❗不再 fallback 到错误路径
            "count": max(1, int(config.get("count", 1))),
            "recursive": bool(config.get("recursive", True)),
        }

    # ─────────────────────────────
    # 图片收集（增强版）
    # ─────────────────────────────
    def _collect_images(self, image_dir: str, recursive: bool) -> list:
        base = Path(image_dir)

        if not image_dir or not base.exists():
            logger.warning(f"[RandomPic] 图片目录不存在: {image_dir}")
            return []

        if not base.is_dir():
            logger.warning(f"[RandomPic] 路径不是目录: {image_dir}")
            return []

        files = set()

        for ext in IMAGE_EXTENSIONS:
            if recursive:
                files.update(base.rglob(f"*{ext}"))
                files.update(base.rglob(f"*{ext.upper()}"))
            else:
                files.update(base.glob(f"*{ext}"))
                files.update(base.glob(f"*{ext.upper()}"))

        # 去重 + 稳定排序
        return sorted(files)

    # ─────────────────────────────
    # 核心发送逻辑
    # ─────────────────────────────
    async def _send_random_images(self, event: AstrMessageEvent, config: dict):
        image_dir = config["image_dir"]
        count = config["count"]
        recursive = config["recursive"]

        images = self._collect_images(image_dir, recursive)

        if not images:
            yield event.plain_result(
                f"❌ 在目录 \"{image_dir}\" 中没有找到任何图片文件。\n"
                "请检查：\n"
                "1. 路径是否正确\n"
                "2. 是否为绝对路径\n"
                "3. 是否包含 jpg/png/gif/webp/bmp 文件"
            )
            return

        selected = random.sample(images, min(count, len(images)))
        random.shuffle(selected)

        logger.info(
            f"[RandomPic] 图片总数 {len(images)}，发送 {len(selected)} 张"
        )

        for img in selected:
            yield event.image_result(str(img))

    # ─────────────────────────────
    # /randompic 指令
    # ─────────────────────────────
    @filter.command("randompic")
    async def command_random_pic(self, event: AstrMessageEvent):
        config = await self._get_config()

        # ❗ 强制检查 image_dir（关键修复）
        if not config.get("image_dir"):
            yield event.plain_result(
                "❌ 未配置 image_dir，请在插件设置中填写：\n"
                "/AstrBot/data/plugins/astrbot_plugin_random_pic/random_pic"
            )
            return

        async for result in self._send_random_images(event, config):
            yield result

    # ─────────────────────────────
    # 关键词触发
    # ─────────────────────────────
    @filter.event_message_type(
        EventMessageType.GROUP_MESSAGE | EventMessageType.PRIVATE_MESSAGE
    )
    async def on_keyword_trigger(self, event: AstrMessageEvent):
        config = await self._get_config()
        keywords = config["keywords"]

        if not keywords:
            return

        msg = event.message_str.strip()

        if msg not in keywords:
            return

        async for result in self._send_random_images(event, config):
            yield result

    async def terminate(self):
        pass
