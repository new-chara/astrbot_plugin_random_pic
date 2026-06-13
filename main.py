import os
import random
from pathlib import Path

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event.filter import EventMessageType
from astrbot.api.star import Context, Star
from astrbot.api import logger

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

# 插件自身目录下的 random_pic 文件夹（绝对路径）
_PLUGIN_DIR = Path(__file__).parent
DEFAULT_IMAGE_DIR = str(_PLUGIN_DIR / "random_pic")


class RandomPicPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _get_config(self) -> dict:
        """Load and return plugin config, with fallback defaults."""
        try:
            config = await self.context.get_config()
            if not isinstance(config, dict):
                config = dict(config) if config else {}
        except Exception:
            config = {}

        # 打印原始配置用于调试
        logger.info(f"[RandomPic] 原始配置: {dict(config)}")

        # 支持旧版 "keyword" 和新版 "keywords"（textarea，每行一个）两种配置
        raw = config.get("keywords") or config.get("keyword") or "随机图片"
        if isinstance(raw, str):
            keywords = [k.strip() for k in raw.replace("\r\n", "\n").split("\n") if k.strip()]
        elif isinstance(raw, list):
            keywords = [str(k).strip() for k in raw if str(k).strip()]
        else:
            keywords = []

        image_dir = config.get("image_dir") or DEFAULT_IMAGE_DIR
        count = max(1, int(config.get("count", 1)))
        recursive = config.get("recursive", True)
        if isinstance(recursive, str):
            recursive = recursive.lower() in ("true", "1", "yes")

        logger.info(
            f"[RandomPic] 配置加载: keywords={keywords}, "
            f"image_dir={image_dir}, count={count}, recursive={recursive}"
        )

        return {
            "keywords": keywords,
            "image_dir": image_dir,
            "count": count,
            "recursive": recursive,
        }

    def _collect_images(self, image_dir: str, recursive: bool) -> list:
        """Collect all image file paths from the given directory.

        Returns a list of pathlib.Path objects.
        """
        base = Path(image_dir)
        if not base.exists():
            logger.warning(f"[RandomPic] 图片目录不存在: {image_dir}")
            return []
        if not base.is_dir():
            logger.warning(f"[RandomPic] 路径不是目录: {image_dir}")
            return []

        files = []
        for ext in IMAGE_EXTENSIONS:
            pattern = f"*{ext}"
            if recursive:
                files.extend(base.rglob(pattern))
                # Also match uppercase on case-sensitive filesystems
                files.extend(base.rglob(f"*{ext.upper()}"))
            else:
                files.extend(base.glob(pattern))
                files.extend(base.glob(f"*{ext.upper()}"))

        # Deduplicate (Path objects are hashable)
        return list(set(files))

    async def _send_random_images(self, event: AstrMessageEvent, config: dict):
        """Core logic: pick random images and yield results."""
        image_dir = config["image_dir"]
        count = config["count"]
        recursive = config["recursive"]

        images = self._collect_images(image_dir, recursive)
        if not images:
            yield event.plain_result(
                f"❌ 在目录 \"{image_dir}\" 中没有找到任何图片文件。\n"
                "请检查路径是否正确，以及目录中是否包含支持的图片格式（jpg/png/gif/webp/bmp）。"
            )
            return

        selected = random.sample(images, min(count, len(images)))
        random.shuffle(selected)

        logger.info(
            f"[RandomPic] 从 {len(images)} 张图片中随机选取 {len(selected)} 张"
        )

        for img_path in selected:
            yield event.image_result(str(img_path))

    # ── /randompic 命令 ──────────────────────────────────────────

    @filter.command("randompic")
    async def command_random_pic(self, event: AstrMessageEvent):
        """使用 /randompic 命令触发随机图片发送。"""
        config = await self._get_config()
        async for result in self._send_random_images(event, config):
            yield result

    # ── 关键字触发监听 ────────────────────────────────────────────

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE | EventMessageType.PRIVATE_MESSAGE)
    async def on_keyword_trigger(self, event: AstrMessageEvent):
        """监听消息，匹配配置的任意关键字触发随机图片发送。"""
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
        """插件卸载时调用。"""
        pass
