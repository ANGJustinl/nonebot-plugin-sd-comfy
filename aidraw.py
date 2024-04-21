import websockets
import uuid
import json
import random
from urllib.parse import urlencode
import aiohttp

from .config import plugin_config


# 设置服务器地址和客户端ID
server_address = plugin_config.server_address
client_id = str(uuid.uuid4())


# 定义向服务器发送提示的函数
async def async_queue_prompt(session, prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    url = "http://{}/prompt".format(server_address)
    async with session.post(url, data=data) as response:
        return await response.json()


# 定义从服务器下载图像数据的函数
async def async_get_image(session, filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)
    url = "http://{}/view?{}".format(server_address, url_values)
    async with session.get(url) as response:
        return await response.read()


# 定义获取历史记录的函数
async def async_get_history(session, prompt_id):
    url = "http://{}/history/{}".format(server_address, prompt_id)
    async with session.get(url) as response:
        return await response.json()


# 定义通过WebSocket接收消息并下载图像的函数
async def get_images(ws, session, prompt):
    prompt_id = await async_queue_prompt(session, prompt)
    prompt_id = prompt_id["prompt_id"]
    while True:
        out = await ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # 执行完成
        else:
            continue  # 预览是二进制数据

    history = await async_get_history(session, prompt_id)
    history = history[prompt_id]
    images_output = []
    for o in history["outputs"]:
        node_output = history["outputs"][o]
        if "images" in node_output:
            for image in node_output["images"]:
                image_data = await async_get_image(
                    session, image["filename"], image["subfolder"], image["type"]
                )
                images_output.append(image_data)
    return images_output


async def aidraw(
    ApiJson,
    CharacterNumber: str,
    CharacterName: str,
    PositiveTags: str,
    NegativeTags: str,
):
    # 创建一个WebSocket连接到服务器
    async with websockets.connect(
        f"ws://{server_address}/ws?clientId={client_id}"
    ) as ws:
        async with aiohttp.ClientSession() as session:
            # 将 api JSON字符串解析为Python字典，并根据需要修改其中的文本提示和种子值
            prompt = ApiJson
            prompt["13"]["inputs"]["string"] = CharacterNumber
            prompt["16"]["inputs"]["string"] = CharacterName
            prompt["17"]["inputs"]["string"] = PositiveTags
            if NegativeTags:
                prompt["20"]["inputs"]["string"] = NegativeTags
            prompt["66"]["inputs"]["noise_seed"] = random.randint(
                1, 18446744073709550591
            )

            # 调用get_images()函数来获取图像
            images = await get_images(ws, session, prompt)
            # 输出图像
            return images
