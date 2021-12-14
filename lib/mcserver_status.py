import requests
import json

def mcserver_status(ip,port=25565):
    r = requests.get("api".format(ip,port))
    jsondata = json.loads(r.text)
    return jsondata