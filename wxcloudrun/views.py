from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import  os
import jieba
import json
import requests

def duixiangcunchu(courseid):
  #获取token
  response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxfb2997f507abf89e&secret=168726b557fb7221c96955cec59b3347',verify=False)
  data ={
    "env": "prod-0gayxkvve034fe60",
    "path": "filecontent/"+courseid+".jpg"
  }
  #return str(response.json())
  #转json
  data = json.dumps(data)
  response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data,verify=False)
  print(response.json())
  #response = json.loads(response.json())
  #得到上传链接

  data2={
    "Content-Type":(None,".jpg"),
    "key": (None,"filecontent/"+courseid+".jpg"),
    "Signature": (None,response.json()['authorization']),
    'x-cos-security-token': (None,response.json()['token']),
    'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
    'file': ('filecontent.jpg',open(r"/app/wxcloudrun/filecontent.jpg","rb"))
  }
  #data2 = json.dumps(data2)
  response2 = requests.post(response.json()['url'], files=data2,verify=False)
  return response.json()["file_id"]

@app.route('/', methods=['POST'])
def upload():
#     stopwords={'我们','你们','他们','它们','因为','因而','所以','如果','那么',
#           '如此','只是','但是','就是','这是','那是','而是','而且','虽然',
#           '这些','有些','然后','已经','于是','一种','一个','一样','时候',
#     '没有','什么','这样','这种','这里','不会','一些','这个','仍然','不是',
#     '自己','知道','可以','看到','那儿','问题','一会儿','一点','现在','两个',
#          '三个','我','的','是','以及','干嘛','用来','很','到底'}
    num = ['1','2','3','4','5','6','7','8','9']
    stopwords = set()
    content = [line.strip() for line in open(r'/app/wxcloudrun/baidu_stopwords.txt','r',encoding="utf-8").readlines()]
    stopwords.update(content)
    stopwords.update(num)
    texts = []

    file = request.json.get('allcomment')
    courseid = request.json.get('courseid')
    text = jieba.lcut(file)
    for item in text:
        if item not in stopwords:
            texts.append(item)
    text = str(texts)
    bg_pic = imread('/app/wxcloudrun/backimage.png')
    wordcloud = WordCloud(mask=bg_pic,background_color='white',font_path='/app/wxcloudrun/华文楷体.ttf',scale=1.5).generate(text)

    wordcloud.to_file('/app/wxcloudrun/filecontent.jpg')

    a = duixiangcunchu(courseid)
    b = {"re":a}
    c = json.dumps(b)
    return c
