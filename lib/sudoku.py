import requests
import json
from PIL import Image, ImageDraw, ImageFont

def sudoku(difficulty):
    r = requests.get("http://apis.juhe.cn/fapig/sudoku/generate?key=142a30dc17d224150da21835284e9b49&difficulty={}".format(difficulty))
    jsontopython = json.loads(r.text)
    shudu = Image.open("D:/Users/Administrator/Desktop/shudu.PNG")
    draw = ImageDraw.Draw(shudu)
    fnt = ImageFont.truetype(r'C:\Windows\Fonts\simkai.ttf',36)
    for i in range(0,9):
        for y in range(0,9):
            if (((jsontopython["result"])["puzzle"])[i])[y] != 0:
                draw.text((((shudu.size[0]/9)*(i)+9),(shudu.size[1]/9)*(y)),str((((jsontopython["result"])["puzzle"])[i])[y]),fill='black',font=fnt)
            else:
                continue
    shudu.save("D:/Users/Administrator/Desktop/shudu1.PNG")