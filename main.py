import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Saya

 
saya = create(Saya)
app = Ariadne(
    connection=config(
        xxxx,  # 机器人的 qq 号
        "xxxx",  # 你的 mirai-api-http 中的 verifyKey
        # 以下两行为 mirai-api-http 中的监听地址
        # 默认为 "http://localhost:8080"
        HttpClientConfig(host="http://127.0.0.1:17380"),
        WebsocketClientConfig(host="http://127.0.0.1:17380"),
    ),
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()