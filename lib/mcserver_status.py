import requests
import json

def mcserver_status(ip,port=25565):
    r = requests.get("http://mcapi.us/server/status?ip={}&port={}".format(ip,port))
    jsondata = json.loads(r.text)
    return jsondata