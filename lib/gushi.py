import requests

def get_gushi():
    r = requests.get("http://api.tianapi.com/verse/index?key=f9780fbde529acd4c49c317d72073039")
    return r.text[r.text.find('content')+10:r.text.find('source')-3]+'\n'+'——《'+r.text[r.text.find('source')+9:r.text.find('author')-3]+'》'+r.text[r.text.find('author')+9:-4]