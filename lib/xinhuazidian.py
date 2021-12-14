import requests
import json

def xinhuazidian(word):
    r = requests.get("api".format(word))
    jsontopython = json.loads(r.text)
    word_out = " "
    for i in (jsontopython["result"])["jijie"]:
        word_out = word_out+"\n"+str(i)
    word_out = word_out+"\n详解:"
    for n in (jsontopython["result"])["xiangjie"]:
        word_out = word_out+"\n"+str(n)