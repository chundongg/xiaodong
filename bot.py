from graia.application.group import Group
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Image, Plain
from graia.application.friend import Friend
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="nwdiowamllwn", # 填入 authKey
        account=2657661565, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

__version__ = 0.1
__author__ = "葱油饼"
__name__ = "小鼕"

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    #向好友发送文字信息
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain("你好，我是小鼕！我于今天出生了！")
    ]))
    #向好友发送图片
    await app.sendFriendMessage(friend, MessageChain.create([
        Image.fromLocalFile("./images/xiaodong/xiaocd.jpg")
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("#课表")])
])
async def group_message_listener(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group,MessageChain.create([
        Image.fromLocalFile("./images/kebiao/kebiao.jpg")    
    ]))

app.launch_blocking()