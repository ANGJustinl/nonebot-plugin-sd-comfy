import io
import json
from nonebot import require

require("nonebot_plugin_alconna")

from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    on_alconna,
    AlconnaMatches,
    Arparma,
    UniMessage,
    Image,
    At,
)

from .config import Config
from .command import DrawCommand
from .aidraw import aidraw

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-sd-comfy",
    description="Generate images with Stable-Diffusion-Comfyui",
    usage="/aidraw + 词条",
    type="application",
    config=Config,
    extra={},
)

# 导入api.json
with open("src/plugins/sd-comfy/api.json", "r", encoding="utf-8") as f:
    ApiJson = json.load(f)


AIDraw = on_alconna(DrawCommand, auto_send_output=True)


@AIDraw.handle()
async def _(Args_out: Arparma = AlconnaMatches()):
    logger.info("画图命令解析: " + str(Args_out))
    if Args_out.matched:
        PositiveTags = Args_out.main_args
        Other_args = Args_out.other_args
        CharacterNumber = "1girl"  # test
        CharacterName = "toki"  # test
        images = await aidraw(ApiJson, CharacterNumber, CharacterName, PositiveTags)
        if images:
            logger.success("SD 绘制成功")
            for image_data in images:
                image = io.BytesIO(image_data)
                await AIDraw.send(
                    UniMessage(
                        ["你的画图结果来啦"],
                        At("user", str(Event.get_user_id)),
                        [Image(raw=image)],
                    ).export()
                )
            logger.success("绘图结果发送成功")
            await AIDraw.finish()
        logger.error("SD 绘制失败")
        await AIDraw.send(UniMessage(["绘制失败"], At("user", str(Event.get_user_id))))
        await AIDraw.finish()

    logger.warning("画图命令解析有误: " + str(Args_out))
    await AIDraw.finish("画图命令有误: " + str(Args_out.error_info))
