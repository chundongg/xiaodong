import asyncio

from graia.application import GraiaMiraiApplication, Session
from graia.saya import Saya
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.broadcast.interrupt import InterruptControl

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
bcc = Broadcast(loop=loop)
saya = Saya(broadcast)
saya.install_behaviours(BroadcastBehaviour(broadcast))
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="nwdiowamllwn", # 填入 authKey
        account=2657661565, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
inc = InterruptControl(bcc)

__version__ = 0.2
__author__ = "葱油饼"
__name__ = "小鼕"

with saya.module_context():
    saya.require("modules.modules_kebiao")

try:
    loop.run_forever()
except KeyboardInterrupt:
    exit()