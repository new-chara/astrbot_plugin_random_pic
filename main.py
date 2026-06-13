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
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}
        logger.info(f"[RandomPic] 插件初始化，配置: {dict(self.config)}")

    def _get_config(self) -> dict:
        """????????????????"""
        raw = self.config.get("keywords") or self.config.get("keyword") or "????"
        if isinstance(raw, str):
            text = raw.replace("\r\n", "\n").replace("?", ",")
            if "\n" in text:
                keywords = [k.strip() for k in text.split("\n") if k.strip()]
            else:
                keywords = [k.strip() for k in text.split(",") if k.strip()]
        elif isinstance(raw, list):
            keywords = [str(k).strip() for k in raw if str(k).strip()]
        else:
            keywords = []

        image_dir = self.config.get("image_dir") or DEFAULT_IMAGE_DIR
        count = max(1, int(self.config.get("count", 1)))
        max_count = max(1, int(self.config.get("max_count", 3)))
        recursive = self.config.get("recursive", True)
        if isinstance(recursive, str):
            recursive = recursive.lower() in ("true", "1", "yes")

        return {
            "keywords": keywords,
            "image_dir": image_dir,
            "count": count,
            "max_count": max_count,
            "recursive": recursive,
        }

    def _parse_count(self, msg: str, keywords: list, max_count: int) -> tuple:
        """??????????????? (matched_keyword, count)?

        ?????“关键字”或“关键字 N”。
        N 超过 max_count 时截断到 max_count。
        """
        msg = msg.strip()
        for kw in keywords:
            if msg == kw:
                return (kw, None)
            if msg.startswith(kw + " "):
                tail = msg[len(kw):].strip()
                try:
                    n = int(tail)
                    if n > 0:
                        return (kw, min(n, max_count))
                except ValueError:
                    pass
        return (None, None)

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
        """使用 /randompic 命令触发，可带数量参数。
        例如 /randompic 或 /randompic 3
        """
        config = self._get_config()
        args = event.get_command_args().strip()
        if args:
            try:
                n = int(args)
                if n > 0:
                    config["count"] = min(n, config["max_count"])
            except ValueError:
                pass
        async for result in self._send_random_images(event, config):
            yield result

    # ── 关键字触发监听 ────────────────────────────────────────────

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE | EventMessageType.PRIVATE_MESSAGE)
    async def on_keyword_trigger(self, event: AstrMessageEvent):
        """监听消息，匹配配置的任意关键字触发随机图片发送。
        支持“关键字 N”格式指定发送数量。
        """
        config = self._get_config()
        keywords = config["keywords"]
        if not keywords:
            return

        matched, count = self._parse_count(
            event.message_str, keywords, config["max_count"]
        )
        if matched is None:
            return
        if count is not None:
            config["count"] = count

        async for result in self._send_random_images(event, config):
            yield result

    async def terminate(self):
        """插件卸载时调用。"""
        pass
