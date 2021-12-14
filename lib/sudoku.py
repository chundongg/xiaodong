import requests
import json
from PIL import Image, ImageDraw, ImageFont

def sudoku(difficulty):
    r = requests.get("api".format(difficulty))
    jsontopython = json.loads(r.text)
    shudu = Image.open("本地文件夹") #本地文件夹
    draw = ImageDraw.Draw(shudu)
    fnt = ImageFont.truetype(r'C:\Windows\Fonts\simkai.ttf',36) #本地字体
    for i in range(0,9):
        for y in range(0,9):
            if (((jsontopython["result"])["puzzle"])[i])[y] != 0:
                draw.text((((shudu.size[0]/9)*(i)+9),(shudu.size[1]/9)*(y)),str((((jsontopython["result"])["puzzle"])[i])[y]),fill='black',font=fnt)
            else:
                continue
    shudu.save("本地文件夹") #本地文件夹