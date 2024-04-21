import io
import json
from nonebot import require

require("nonebot_plugin_alconna")

from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    on_alconna,
    AlconnaMatches,
    Arparma,
    UniMessage,
    Image,
)

from .config import Config
from .command import DrawCommand
from .aidraw import aidraw
from .utils import extract_tags

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-sd-comfy",
    description="Generate images with Stable-Diffusion-Comfyui",
    usage="/aidraw + 词条",
    type="application",
    config=Config,
    extra={},
)

# 导入api.json
with open("src/plugins/nonebot-plugin-sd-comfy/api.json", "r", encoding="utf-8") as f:
    ApiJson = json.load(f)


AIDraw = on_alconna(DrawCommand, auto_send_output=True)


@AIDraw.handle()
async def _(Args_out: Arparma = AlconnaMatches()):
    logger.info("画图命令解析: " + str(Args_out))
    if Args_out.matched:
        PositiveTags = Args_out.main_args
        Other_args = Args_out.other_args
        # 调用函数并打印结果
        CharacterNumber, PositiveTags = extract_tags(PositiveTags)
        CharacterName = ""  # test
        NegativeTags = Other_args.get("NegativeTags")
        await AIDraw.send("命令解析为: "+str(Args_out)+" 开始绘画")
        images = await aidraw(
            ApiJson, CharacterNumber, CharacterName, PositiveTags, NegativeTags
        )
        if images:
            logger.success("SD 绘制成功")
            for image_data in images:
                image = io.BytesIO(image_data)
                await AIDraw.send(
                    await UniMessage(
                        ["你的画图结果来啦", Image(raw=image)],
                    ).export(),
                    at_sender=True,
                )
            logger.success("绘图结果发送成功")
            await AIDraw.finish()
        logger.error("SD 绘制失败")
        await AIDraw.send("SD 后端绘制失败", at_sender=True)
        await AIDraw.finish()

    logger.warning("画图命令解析有误: " + str(Args_out))
    await AIDraw.finish("画图命令有误: " + str(Args_out.error_info))
