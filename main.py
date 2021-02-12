# coding: UTF-8
import collections
import time
import datetime
import json
import requests
import decimal
import sys
import schedule
from recruitingbot import RecruitingBot

def BeforeExam():
        thread = api.GetNewMessage(group_id)
        if thread != 0:
                user_id = thread[0]["user"]["uid"]
                chat_id = thread[0]["id"]
                api.PostFirstReply(group_id,chat_id)
                while True:
                        i = api.GetFirstReplyGooBoo(group_id,chat_id)
                        if i == 3:
                                api.PostGooBooError(group_id,chat_id)
                        elif i == 1 or i== 2:
                                break
                        time.sleep(3)
                if i == 2:
                        api.PostCallAdmin(group_id,chat_id,admin_room_id)
                elif i == 1:
                        api.PostAskIGN(group_id,chat_id)
                        reply_number = 3
                        while True:
                                while True:
                                        result = api.GetIGN(group_id,chat_id,reply_number)
                                        time.sleep(3)
                                        if result != None:
                                                ign = result
                                                data = api.GetIGNData(application_id,ign,wg_access_token)
                                                break
                                data = api.GetIGNData(application_id,ign,wg_access_token)
                                if data == None:
                                        api.PostIGNError(group_id,chat_id)
                                        reply_number += 2
                                else:
                                        battles = data["statistics"]["all"]["battles"]
                                        wins = data["statistics"]["all"]["wins"]
                                        decimal.getcontext().prec = 4 
                                        winrate = decimal.Decimal(wins)/decimal.Decimal(battles)*100
                                        last_battle_time = datetime.datetime.fromtimestamp(data["last_battle_time"])
                                        nickname = data["nickname"]
                                        api.PostAskOK(group_id,chat_id,battles,nickname)
                                        while True:
                                                i = api.GetAskOKGooBoo(group_id,chat_id)
                                                if i == 1 or i == 2:
                                                        break
                                                elif i == 3:
                                                        api.PostGooBooError(self,group_id,chat_id)
                                                time.sleep(3)
                                        if i == 1:
                                                break
                                        elif i == 2:
                                                api.PostAskIGN(group_id,chat_id)
                                                reply_number += 3
        
                        api.PostWhichClan(group_id,chat_id)
                        reply_number += 3
                        while True:
                                result = api.GetWhichClan(group_id,chat_id,reply_number)
                                if result != None:
                                        clan_number = result
                                        break
                                time.sleep(3)
                        clan = clans[clan_number]
                        api.PostStartExam(group_id,chat_id,admin_room_id,battles,winrate,last_battle_time,nickname,clan)
        
reload(sys)
sys.setdefaultencoding("utf-8")
group_id = "587e17a3ab0b640e62fb444b3c48b83832b622e7"
admin_room_id = "0fa5904919f14152cbb50d427922b470e68af0ee"
application_id = "eda85c3d6ddbb56920d3544319a4a788"
wg_access_token = "9a72b04b7f60bffc904503e93c241110dd080e4f"
clans = {"1":"WWN","2":"WWN-2","3":"WWN-3","4":"WWN-4","5":"WWN-A","6":"WWN-E"}
#ign = "TAI_seisen_shokuhin_7171"

api = RecruitingBot()
api.Login("taiseimaruyama7171@gmail.com", "maru0807171")

schedule.every(3).seconds.do(BeforeExam)

while True:
        schedule.run_pending()
        time.sleep(1)



