from pydantic import Extra, BaseModel

from nonebot import get_plugin_config


class Config(BaseModel, extra=Extra.ignore):
    negative_default: str = "nsfw, lowres, bad anatomy, bad hands, text, error, 5 fingers, 6 fingers, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"
    server_address: str = "127.0.0.1:8188"


plugin_config = get_plugin_config(Config)
