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

#获取文件
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
    filename =download_url.split("/")[-1]
    f = requests.get(download_url)
    path = "/app/wxcloudrun/"+filename
    #下载文件
    with open(path,"wb") as code:
         code.write(f.content)
    return path

@app.route('/', methods=['POST'])
def upload():
    gbm = lgb.Booster(model_file='/app/wxcloudrun/model.txt')
    fileid = request.json.get('fileid')
    path = getfile(fileid)
    data = pd.read_csv(path, encoding="utf-8")
    student_ID =  data['student_ID']
    data.drop(columns = ['student_ID'], inplace = True)
    data.fillna(-1, inplace = True)
    y_pred = gbm.predict(data, num_iteration=gbm.best_iteration)
    a = []
    k = 0
    for item in y_pred:
        if item >= 0.5:
            a.append(1)
        else:
            a.append(0)
            k += 1
    ob = {}
    for i,j in zip(a,student_ID):
        ob[j] = i
    c = json.dumps(ob)
    return c
