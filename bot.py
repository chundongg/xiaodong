from graia.application.group import Group, Member
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import random
import re

from lib.qiandao import picture_spell

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


@bcc.receiver("GroupMessage")
async def help(app: GraiaMiraiApplication, group: Group,message: MessageChain):
    if message.asDisplay().startswith("#help"):
        await app.sendGroupMessage(group,message.create([
            Plain("你好，小鼕指令集:\n============\n#help - 打开小鼕指令集\n#摇签 - 小鼕摇签中~\n#课表 - 获取课表\n#随机吃饭 - 小鼕帮你选择饭店\n#帮我选择 选择A 选择B ..\n- 小鼕帮你从选择A与选择B以及其他选择中选择\n#随机二次元 - 不可以色色")
        ]))

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
    if message.asDisplay().startswith("#帮我选择 "):
        word = re.sub("[^\w]", " ", message.asDisplay().replace("#帮我选择 ","")).split()
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("小鼕帮你选择：{}".format(random.choice(word)))
        ]))

@bcc.receiver("GroupMessage",dispatchers=[
    Kanata([FullMatch("#随机二次元")])
])
async def randompic(
    message:MessageChain,
    app: GraiaMiraiApplication,
    group:Group
):

#http://api.mtyqx.cn/api/random.php
#https://img.xjh.me/random_img.php (850+) 出处(・ω・)ノ
#http://www.dmoe.cc/random.php（1000+）出处(・ω・)ノ
#https://acg.yanwz.cn/api.php (400+) 出处(・ω・)ノ
#https://img.paulzzh.tech/touhou/random (东方的随机图，43000+)出处(・ω・)ノ
#https://acg.toubiec.cn/random.php（1000+） 出处(・ω・)ノ 作者开源了 这篇博客里有介绍和源码 先蟹蟹大佬了[项目]随机二次元图片API-已经开源

    await app.sendGroupMessage(group,message.create([
        Plain("正在下载中，请稍等")
    ]))
    await app.sendGroupMessage(group,message.create([
        Image.fromNetworkAddress("http://www.dmoe.cc/random.php")
    ]))

@bcc.receiver("GroupMessage",dispatchers=[
    Kanata([FullMatch("#摇签")])
])
async def qiandao(
    message:MessageChain,
    app: GraiaMiraiApplication,
    group:Group,member:Member,
):
    await app.sendGroupMessage(group,message.create([
        Plain("正在摇签中~~")
    ]))
    picture_spell(member.id,member.name)
    await app.sendGroupMessage(group,message.create([
        Image.fromLocalFile("D:/Users/Administrator/Desktop/file.png")
    ]))

app.launch_blocking()