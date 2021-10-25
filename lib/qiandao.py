import os
import requests
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def picture_spell(id,name):
    # 获取到图片格式的文件的路径，此路径为图片所在的文件夹
    r = requests.get("https://api.fanlisky.cn/api/qr-fortune/get/{}".format(id))
    r1 = requests.get("https://v1.hitokoto.cn")
    response = requests.get("http://www.dmoe.cc/random.php")
    image = Image.open(BytesIO(response.content))
    image.save('D:/xiaochun/xiaochun/images/qiandao/get.jpg')
    path = "D:/xiaochun/xiaochun/images/qiandao"
    result = []
    file_name_list = os.listdir(path)
    for file in file_name_list:
        if os.path.isfile(os.path.join(path, file)):
            if file.split(".")[1] in ['jpg', 'png']:
                result.append(os.path.join(path, file))

    ims = list()
    for fn in result:
        ims.append(Image.open(fn))

    # 获取各自的宽,高
    width_one, height_one = ims[0].size
    width_two, height_two = ims[1].size

    # 将两张图片转化为相同宽度的图片
    new_img_one = ims[0].resize((1920, height_one), Image.BILINEAR)
    new_img_two = ims[1].resize((1920, height_two), Image.BILINEAR)

    # 创建一个新图片,定义好宽和高
    target_images = Image.new('RGB', (1920, height_one + height_two))
    target_images.paste(new_img_two, (0, 0, 1920, height_two))
    target_images.paste(new_img_one, (0, height_two, 1920, height_one + height_two))
    
    # 注意存储路径
    draw = ImageDraw.Draw(target_images)
    fnt = ImageFont.truetype(r'C:\Windows\Fonts\simkai.ttf',72)
    fortuneSummary = "今天运势："+r.text[r.text.find("fortuneSummary")+17:r.text.find("luckyStar")-3]
    luckyStar = r.text[r.text.find("luckyStar")+12:r.text.find("signText")-3]
    signText = r.text[r.text.find("signText")+11:r.text.find("unSignText")-3]
    xiaodong = "随机生成，请勿迷信\n           by@小鼕"
    yiyan = r1.text[r1.text.find("hitokoto")+11:r1.text.find("type")-3]+"\n——"+r1.text[r1.text.find("from_who")+10:r1.text.find("creator")-2]
    if len(yiyan) > 24 :
        li = list(yiyan)
        li.insert(24,'\n')
        yiyan = ''.join(li)
        if len (yiyan) > 49 :
            li = list(yiyan)
            li.insert(49,'\n')
            yiyan = ''.join(li)
            if len (yiyan) > 74 :
                li = list(yiyan)
                li.insert(74,'\n')
                yiyan = ''.join(li)
                if len (yiyan) > 99 :
                    li = list(yiyan)
                    li.insert(99,'\n')
                    yiyan = ''.join(li)
    draw.text((target_images.size[0]/14,(target_images.size[1]/14)*8),"@"+name,fill='black',font=fnt)
    draw.text((target_images.size[0]/14*12,(target_images.size[1]/14)*8),time.strftime("%m/%d", time.localtime()),fill='black',font=fnt)
    draw.text((target_images.size[0]/14,(target_images.size[1]/14)*9),yiyan,fill='black',font=fnt)
    draw.text((target_images.size[0]/14,(target_images.size[1]/14)*11),fortuneSummary,fill='black',font=fnt)
    draw.text((target_images.size[0]/14,(target_images.size[1]/14)*12),luckyStar,fill='black',font=fnt)
    draw.text((target_images.size[0]/14,(target_images.size[1]/14)*13),signText,fill='black',font=fnt)
    draw.text((target_images.size[0]/14*12,(target_images.size[1]/18)*17),xiaodong,fill='black',font=ImageFont.truetype(r'C:\Windows\Fonts\simkai.ttf',28))
    target_images.save("D:/Users/Administrator/Desktop/file.png")