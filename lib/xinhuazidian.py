import requests
import json

def xinhuazidian(word):
    r = requests.get("http://v.juhe.cn/xhzd/query?key=5afc554b97cb95ab7a6c646da885d9b5&word={}".format(word))
    jsontopython = json.loads(r.text)
    word_out = " "
    for i in (jsontopython["result"])["jijie"]:
        word_out = word_out+"\n"+str(i)
    word_out = word_out+"\n详解:"
    for n in (jsontopython["result"])["xiangjie"]:
        word_out = word_out+"\n"+str(n)