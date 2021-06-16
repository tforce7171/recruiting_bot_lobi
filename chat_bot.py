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

def LookieInterview(group_id):
        chat_id = GetChatID(group_id)
        api.PostFirstReply(group_id,chat_id)
        gooboo = WaitGooBoo(chat_id)
        if gooboo == 2:
                api.PostCallAdmin(group_id,chat_id,admin_room_id)
                return
        elif gooboo == 1:
                ign_data = ClarifyIGN(group_id,chat_id)
                clan = GetDesireClan(group_id,chat_id,ign_data)
                exam_chat_id = api.PostStartExam(group_id,chat_id,admin_room_id,ign_data,clan)
                return exam_chat_id
# def AdminExam():
def ClarifyIGN(group_id,chat_id):
        api.PostAskIGN(group_id,chat_id)
        reply_number = 3
        while True:
                ign = WaitReply(group_id,chat_id,reply_number)
                ign_data = api.GetIGNData(application_id,ign)
                if ign_data == None:
                        api.PostIGNError(group_id,chat_id)
                        reply_number += 2
                else:
                        api.PostAskOK(group_id,chat_id,ign_data["battles"],ign_data["nickname"])
                        i = WaitGooBoo(chat_id)
                        if i == 1:
                                ign_data["reply_number"] = reply_number
                                return ign_data
                        elif i == 2:
                                reply_number += 3
                                api.PostAskIGN(group_id,chat_id)
def GetDesireClan(group_id,chat_id,ign_data):
        api.PostWhichClan(group_id,chat_id)
        reply_number = ign_data["reply_number"]
        reply_number += 3
        while True:
                reply = WaitReply(group_id,chat_id,reply_number)
                if reply in ["1","2","3","4","5","6"]:
                        clan_number = reply
                        clans = {"1":"WWN","2":"WWN-2","3":"WWN-3","4":"WWN-4","5":"WWN-A","6":"WWN-E"}
                        clan = clans[clan_number]
                        return clan
                else:
                        api.PostClanNumberError(group_id,chat_id)
                        reply_number += 2
def WaitReply(group_id,chat_id,reply_number):
        while True:
                result = api.GetReply(group_id,chat_id,reply_number)
                if result != None:
                        break
                time.sleep(3)
        return result
def WaitGooBoo(chat_id):
        while True:
                i = api.GetLastReplyGooBoo(group_id,chat_id)
                if i == 3:
                        api.PostGooBooError(group_id,chat_id)
                elif i == 1 or i== 2:
                        return i
                time.sleep(3)
def GetUserID(group_id):
        thread = api.GetNewMessage(group_id)
        user_id = thread[0]["user"]["uid"]
        return user_id
def GetChatID(group_id):
        thread = api.GetNewMessage(group_id)
        chat_id = thread[0]["id"]
        return chat_id

if __name__ == "__main__":
        reload(sys)
        sys.setdefaultencoding("utf-8")
        # group_id = "587e17a3ab0b640e62fb444b3c48b83832b622e7"#production env
        # admin_room_id = "0fa5904919f14152cbb50d427922b470e68af0ee"#production env
        group_id = "587e17a3ab0b640e62fb444b3c48b83832b622e7"#test env
        admin_room_id = "44e42c989a9073148caf0da6b9bef1bbcc580a6d"#test env
        application_id = "eda85c3d6ddbb56920d3544319a4a788"
        clans = {"1":"WWN","2":"WWN-2","3":"WWN-3","4":"WWN-4","5":"WWN-A","6":"WWN-E"}
        api = RecruitingBot()
        api.Login("taiseimaruyama7171@gmail.com", "maru0807171")
        print("constant set")
        exam_chat_id = LookieInterview(group_id)



# thread = api.GetNewMessage(group_id)
# user_id = thread[0]["user"]["uid"]
# chat_id = thread[0]["id"]
# api.PostFirstReply(group_id,chat_id)
# while True:
#         i = api.GetFirstReplyGooBoo(group_id,chat_id)
#         if i == 3:
#                 api.PostGooBooError(group_id,chat_id)
#         elif i == 1 or i== 2:
#                 break
#         time.sleep(3)
# if i == 2:
#         api.PostCallAdmin(group_id,chat_id,admin_room_id)
# elif i == 1:
#         api.PostAskIGN(group_id,chat_id)
#         reply_number = 3
#         while True:
#                 while True:
#                         result = api.GetIGN(group_id,chat_id,reply_number)
#                         time.sleep(3)
#                         if result != None:
#                                 ign = result
#                                 data = api.GetIGNData(application_id,ign,wg_access_token)
#                                 break
#                 data = api.GetIGNData(application_id,ign,wg_access_token)
#                 if data == None:
#                         api.PostIGNError(group_id,chat_id)
#                         reply_number += 2
#                 else:
#                         battles = data["statistics"]["all"]["battles"]
#                         wins = data["statistics"]["all"]["wins"]
#                         decimal.getcontext().prec = 4
#                         winrate = decimal.Decimal(wins)/decimal.Decimal(battles)*100
#                         last_battle_time = datetime.datetime.fromtimestamp(data["last_battle_time"])
#                         nickname = data["nickname"]
#                         api.PostAskOK(group_id,chat_id,battles,nickname)
#                         while True:
#                                 i = api.GetAskOKGooBoo(group_id,chat_id)
#                                 if i == 1 or i == 2:
#                                         break
#                                 elif i == 3:
#                                         api.PostGooBooError(self,group_id,chat_id)
#                                 time.sleep(3)
#                         if i == 1:
#                                 break
#                         elif i == 2:
#                                 api.PostAskIGN(group_id,chat_id)
#                                 reply_number += 3
#         api.PostWhichClan(group_id,chat_id)
#         reply_number += 3
#         while True:
#                 result = api.GetWhichClan(group_id,chat_id,reply_number)
#                 if result != None:
#                         if result == "1" or result == "2" or result == "3" or result == "4" or result == "5" or result == "6":
#                                 clan_number = result
#                                 break
#                         else:
#                                 api.PostClanNumberError(group_id,chat_id)
#                                 reply_number += 2
#                 time.sleep(3)
#         clan = clans[clan_number]
#         api.PostStartExam(group_id,chat_id,admin_room_id,battles,winrate,last_battle_time,nickname,clan)
#         while True:
#                 i = api.GetExamGooBoo(group_id,chat_id)
#                 if i == 3:
#                         api.PostGooBooError(group_id,chat_id)
#                 elif i == 1 or i== 2:
#                         break
#                 time.sleep(3)
