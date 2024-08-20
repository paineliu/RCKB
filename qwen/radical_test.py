from time import sleep
import requests
import json
import os

def http_post(ip, port, path, query):
    url = 'http://%s:%s/%s' % (ip, port, path)
    print(url)
    try:
        r = requests.post(url=url, data=query)
        return r.text
    except:
        return ""
    
def test_chat(ip, port, message):
    
    query_json = {}
    query_json['text'] = message
    ret = http_post(ip, port, 'radical', json.dumps(query_json))
    print(ret)
    print()


if __name__ == "__main__":

    test_chat('127.0.0.1', '8105', "上面两个方下面一个土")
