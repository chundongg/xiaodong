import asyncio

from graia.saya import Saya
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)
saya.install_behaviours(BroadcastBehaviour(broadcast))

with saya.module_context():
    saya.require("./modules/modules_kebiao.py")

try:
    loop.run_forever()
except KeyboardInterrupt:
    exit()