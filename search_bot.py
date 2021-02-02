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
                chat_id = thread[0]["id"]
                user_id = thread[0]["user"]["uid"]
                print(chat_id)
                if not user_id in commander_ids:
                        subprocess.Popen(["python","recruiting_bot_lobi/chat_bot.py","&"])
                        print "starting chat"
reload(sys)
sys.setdefaultencoding("utf-8")
# group_id = "f2ffbb85d8d3cda3e40b9d39cc83e9f93acbec57"#本番
#group_id = "587e17a3ab0b640e62fb444b3c48b83832b622e7"#テスト1
group_id = "52edc23e5931fffb8686379496d55f6950fdf152"#test2
#commander_ids = ["1"]
commander_ids = ["84f798239a13f0e4e5a0d0e02908bf7bf23243ea","dfa384ff8001976885386af1a2b19b510e3d9d33","dfc77ba9f4f1ad110e16397d5db83882f4e6b023","f20e962ed7d10e8e16d50603e6780e33aead6525","149b5334e2c1c6698eb92e9d11151bafe875f952","9a3fde4eab436655099e6d4bd48dcf5f3f02e002","0973f47e4aea29c67194c2265b736abe049cb74c","8f8f0d774ef67d5f0df283105c51f5472d49a385","69c652ac47ce004cf28c74ae6309401f35767894","84d29cfcb67b9d1db02906c915f6a1e22d71b9f6","d3c675a207feedd2ede97bc84fae769ff81bfecf"]
api = RecruitingBot()
api.Login("taiseimaruyama7171@gmail.com", "maru0807171")

schedule.every(3).seconds.do(BeforeExam)

while True:
        schedule.run_pending()
        time.sleep(1)
