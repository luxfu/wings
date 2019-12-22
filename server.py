# coding=utf-8
 
from flask import Flask
import json

app_server = Flask(__name__)
 
"""
这是一个展示Flask如何读取服务器本地文件, 并返回json数据流给前端显示的例子
"""

def loadJson(local_path) -> bytes:
    """
    工具函数:
    获取本地文件内容并转换成json格式
    """
    with open(local_path, 'r') as f:
        data = f.read()
        #data = json.dumps(data)
    return data

@app_server.route('/<url>')
def urlCall(url):
    path = './data.ini'
    data = eval(loadJson(path))
    try:
        return data['/' + url]
    except Exception as e:
        return('没有匹配的url:%s'%e)

def runApp(address, port):
    app_server.run(host=address, debug=True, port=eval(port), use_reloader=False)
 
if __name__ == '__main__':
    app_server.run(host='0.0.0.0', debug=True, port=8080)
    #print(loadJson('./data.ini'))