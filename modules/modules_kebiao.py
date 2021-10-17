from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya.event import SayaModuleInstalled
from graia.saya.builtins.broadcast import ListenerSchema
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image, Plain
from graia.application.group import Group
from graia.application.event.messages import GroupMessage

saya = Saya.current()
channel = Channel.current()

@channel.use(ListenerSchema(
    listening_events=[SayaModuleInstalled]
))
async def module_listener(event: SayaModuleInstalled):
    print(f"{event.module}::课表模块加载成功!!!")

@channel.use(
    ListenerSchema(
        listening_events=[SayaModuleInstalled]
        )
    )
async def module_kebiao_group(event: GroupMessage,app: GraiaMiraiApplication, group: Group):
    print("课表模块被触发!")
    await app.sendGroupMessage(group,MessageChain.create([
        Plain("你好"),Image.fromLocalFile("../images/kebiao/kebiao.jpg")    
    ]))
