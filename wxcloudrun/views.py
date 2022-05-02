from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import lightgbm as lgb

def getfile(fileid):
    response = requests.get( 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxfb2997f507abf89e&secret=168726b557fb7221c96955cec59b3347', )
    access_token = response.json()['access_token']
    data ={
        "env": "prod-0gayxkvve034fe60",
        "file_list": [
        {
          "fileid":fileid,
          "max_age":86400
        }
        ]
      }
    #转json
    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    print(data)
    response = requests.post("https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=" + access_token,data,)
    print(response.json())
    download_url = response.json()['file_list'][0]['download_url']
    f = requests.get(download_url)
    #下载文件
    with open(r"/app/wxcloudrun/11.xlsx","wb") as code:
         code.write(f.content)

@app.route('/', methods=['POST'])
def upload():
    gbm = lgb.Booster(model_file='/app/wxcloudrun/model.txt')
    fileid = request.json.get('fileid')
    
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
