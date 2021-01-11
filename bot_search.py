# coding: UTF-8
import collections
import time
import datetime
import json
import requests
import decimal
import sys
import schedule
import subprocess
from recruitingbot import RecruitingBot

def BeforeExam():
        thread = api.GetNewMessage(group_id)
        if thread != 0:
                subprocess.call(["python","bot_chats.py","&"])
        
reload(sys)
sys.setdefaultencoding("utf-8")
group_id = "587e17a3ab0b640e62fb444b3c48b83832b622e7"

api = RecruitingBot()
api.Login("taiseimaruyama7171@gmail.com", "maru0807171")

schedule.every(3).seconds.do(BeforeExam)

while True:
        schedule.run_pending()
        time.sleep(1)



