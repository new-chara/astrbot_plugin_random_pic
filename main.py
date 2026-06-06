import os
import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.star.filter.command import CommandFilter
from astrbot.core.star.star import star_map
from astrbot.core.star.star_handler import star_handlers_registry
from astrbot.core.utils.astrbot_path import get_astrbot_data_path


# 配置 schema —— 定义 Web 面板上显示的配置项
_CONFIG_SCHEMA = {
    "pics_dir": {
        "description": "图片存放目录（绝对路径）",
        "type": "string",
        "default": os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pics"),
    },
    "triggers": {
        "description": "触发命令列表",
        "type": "list",
        "default": ["randompic", "来张图", "随机图片"],
    },
    "max_count": {
        "description": "每次最多发送图片数量（≤3）",
        "type": "int",
        "default": 3,
    },
}


@register("astrbot_plugin_random_pic", "new_chara", "从本地目录随机发送图片，支持 Web 面板配置", "1.2.0")
class RandomPicPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

        # 创建 AstrBot 官方配置实例（自动生成 JSON 文件，Web 面板可编辑）
        config_path = os.path.join(
            get_astrbot_data_path(), "config", "astrbot_plugin_random_pic.json"
        )
        self._cfg = AstrBotConfig(config_path=config_path, schema=_CONFIG_SCHEMA)

        # 注册到插件元数据，使 Web 面板能读取
        md = star_map.get(self.__class__.__module__)
        if md:
            md.config = self._cfg

    async def initialize(self):
        """初始化：确保图片目录存在，注册触发词别名"""
        os.makedirs(self._cfg.pics_dir, exist_ok=True)
        logger.info(f"[RandomPic] 图片目录: {self._cfg.pics_dir}")
        logger.info(f"[RandomPic] 触发命令: {self._cfg.triggers}, 最大数量: {self._cfg.max_count}")

        self._register_aliases()

    def _register_aliases(self):
        """将配置中的额外触发词注册为命令别名"""
        handler_full_name = f"{self.__class__.__module__}_randompic"
        md = star_handlers_registry.get_handler_by_full_name(handler_full_name)
        if md is None:
            logger.warning(f"[RandomPic] 未找到 Handler: {handler_full_name}")
            return
        for flt in md.event_filters:
            if isinstance(flt, CommandFilter) and flt.command_name == "randompic":
                extra = {
                    t for t in self._cfg.triggers if t and t != "randompic"
                }
                flt.alias.update(extra)
                flt._cmpl_cmd_names = None
                logger.info(f"[RandomPic] 已注册别名: {extra}")
                break

    def _get_images(self) -> list[str]:
        """获取图片目录下所有图片文件"""
        valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
        if not os.path.exists(self._cfg.pics_dir):
            return []
        return [
            os.path.join(self._cfg.pics_dir, f)
            for f in os.listdir(self._cfg.pics_dir)
            if os.path.splitext(f)[1].lower() in valid_exts
        ]

    @filter.command("randompic")
    async def randompic(self, event: AstrMessageEvent, count: int = 1):
        """发送随机图片

        Args:
            event: 消息事件
            count: 发送数量
        """
        count = max(1, min(count, self._cfg.max_count))

        images = self._get_images()
        if not images:
            yield event.plain_result("😿 没有找到图片，请检查 pics_dir 配置。")
            return

        selected = random.sample(images, min(count, len(images)))
        result = event.make_result()
        for img_path in selected:
            result.file_image(img_path)
        yield result

    async def terminate(self):
        logger.info("[RandomPic] 插件已卸载")
