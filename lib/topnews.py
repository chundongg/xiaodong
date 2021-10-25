import json
import requests

def topnews_dayli(keyword="top"):
    r = requests.get("http://v.juhe.cn/toutiao/index?type={}&key=1588f762e5527ba9c4c3545a0319dc81".format(keyword))
    jsontopython = json.loads(r.text)
    word_out = "今日新闻:"
    for i in range(5):
        word_out = word_out+"\n"+(((jsontopython["result"])["data"])[i])['author_name']+'：'+(((jsontopython["result"])["data"])[i])['title']+'\n地址：'+(((jsontopython["result"])["data"])[i])['url']
    return word_out