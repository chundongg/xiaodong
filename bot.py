from graia.application.group import Group, Member
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import random
import re

from graia.application.message.elements.internal import Image, Plain
from graia.application.friend import Friend
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.broadcast.interrupt import InterruptControl
from graia.application.interrupts import GroupMessageInterrupt

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
inc = InterruptControl(bcc)

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

@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorator 混起来
    Kanata([FullMatch("#随机吃饭")])
])
async def group_message_listener(app: GraiaMiraiApplication, group: Group):
    qingfan = random.randint(1,1001)
    if qingfan == 2:
        await app.sendGroupMessage(group,MessageChain.create([
            Plain("今天该吃：{},今天国民请吃饭".format(random.choice(["豆浆记忆","一楼打菜","香锅","饺子","重庆面","黄焖鸡","早餐店左","烤盘","淮南牛肉面","石锅","拉面","烤肉拌饭","清食","水果捞","二楼打菜","汉堡","烤鸭","麻辣烫"])))  
        ]))
    else:
        await app.sendGroupMessage(group,MessageChain.create([
            Plain("今天该吃：{}".format(random.choice(["豆浆记忆","一楼打菜","香锅","饺子","重庆面","黄焖鸡","早餐店左","烤盘","淮南牛肉面","石锅","拉面","烤肉拌饭","清食","水果捞","二楼打菜","汉堡","烤鸭","麻辣烫"])))  
        ]))
@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if message.asDisplay().startswith("测试"):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("发送 /confirm 以继续运行")
        ]))
        #中断
        await inc.wait(GroupMessageInterrupt(
            group, member,
            custom_judgement=lambda x: x.messageChain.asDisplay().startswith("/confirm")
        ))
        #中断
        await app.sendGroupMessage(group, MessageChain.create([
            #At(member.id)输出报错
            Image.fromLocalFile("./images/kebiao/kebiao.jpg") ,Plain("执行完毕.")
        ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if message.asDisplay().startswith("#帮我选择"):
        word = re.sub("[^\w]", " ", message.asDisplay().replace("#帮我选择 ","")).split()
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("小鼕帮你选择：{}".format(random.choice(word)))
        ]))

app.launch_blocking()