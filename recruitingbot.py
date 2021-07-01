# coding: UTF-8
import collections
import time
import datetime
import json
import requests
import decimal
import sys
import schedule
import psycopg2
import os
from photon import LobiAPI

class RecruitingBot(LobiAPI):
#        def __init__(self):
#                self.Login("taiseimaruyama7171@gmail.com", "maru0807171")
        def GetWGAccessToken(self):
                url = "https://tokenrefresher.herokuapp.com/active_token"
                response = requests.get(url)
                wg_access_token = response.json()
                return wg_access_token
        def UpdateAccessToken(self,application_id):
                dict_data = json.load(open('wg_access_token.json', 'r'))
                url = "https://api.worldoftanks.asia/wot/auth/prolongate/"
                body = {
                        "application_id": application_id,
                        "access_token": dict_data["wg_access_token"]
                }
                response = requests.post(url,data=body)
                data = response.json()
                dict_data["wg_access_token"] = data["data"]["access_token"]
                print(dict_data)
                with open('wg_access_token.json', mode='wt') as file:
                        json.dump(dict_data, file, ensure_ascii=False, indent=2)
        def GetNewMessage(self,group_id):
                top_thread = self.GetThreads(group_id,1)
                if top_thread[0].get('replies')==None:
                        return top_thread
                else:
                        return 0
        def PostFirstReply(self,group_id,chat_id):
                message = "[BOTより返信]\nWWN広報室へようこそ\n入隊希望の方はこのメッセージにグーを、\nそれ以外の場合はブーをお願いします"
                response = self.PostReply(group_id,chat_id,message)
        def GetLastReplyGooBoo(self,group_id,chat_id):
                replies = self.GetRepliesAll(group_id,chat_id)
                last_reply = replies["chats"][0]
                goo = last_reply["likes_count"]
                boo = last_reply["boos_count"]
                if goo == "0" and boo == "0":
                    return 0
                elif goo == "1" and boo == "0":
                    return 1
                elif goo == "0" and boo == "1":
                    return 2
                else:
                    return 3
        def PostGooBooError(self,group_id,chat_id):
                message = "[BOTより返信]\nグーブーの入力が不適切です\nどちらかを一度だけ押してください"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostAskIGN(self,group_id,chat_id):
                message = "[BOTより返信]\n入隊希望ですね\nあなたのIGNを返信欄に入力して下さい\nプログラムで検索しますので入力ミスのないようお願いします"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostCallAdmin(self,group_id,chat_id,admin_room_id):
                message = "[BOTより返信]\n入隊以外の要件ですね\n担当者を呼び出します"
                response = self.PostReply(group_id,chat_id,message)
                message = "[BOTより送信]\n広報室に入隊以外の要件の方がいらっしゃいます\n対応お願いします"
                response = self.PostMessage(admin_room_id,message)
                return response
        def GetReply(self,group_id,chat_id,reply_number):
                replies = self.GetRepliesAll(group_id,chat_id)
                replies_count = len(replies["chats"])
                if replies_count == reply_number:
                        return replies["chats"][0]["message"]
                else:
                        return None
        def GetIGNData(self,application_id,ign):
                wg_access_token = self.GetWGAccessToken()
                url = "https://api.wotblitz.asia/wotb/account/list/?application_id={application_id}&search={ign}".format(application_id=application_id,ign=ign)
                response = requests.get(url)
                data = response.json()
                if data["status"] == "error":
                        return None
                else:
                        if data["meta"]["count"] == 0:
                                return None
                        else:
                                account_id = data["data"][0]["account_id"]
                                url = "https://api.wotblitz.asia/wotb/account/info/?application_id={application_id}&account_id={account_id}&access_token={wg_access_token}".format(application_id=application_id,account_id=account_id,wg_access_token=wg_access_token)
                                response = requests.get(url)
                                data = response.json()
                                print(data)
                                ign_data = {}
                                ign_data["battles"] = data["data"][str(account_id)]["statistics"]["all"]["battles"]
                                if ign_data["battles"] == 0:
                                        return None
                                wins = data["data"][str(account_id)]["statistics"]["all"]["wins"]
                                decimal.getcontext().prec = 4
                                ign_data["winrate"] = decimal.Decimal(wins)/decimal.Decimal(ign_data["battles"])*100
                                ign_data["last_battle_time"] = datetime.datetime.fromtimestamp(data["data"][str(account_id)]["last_battle_time"])
                                ign_data["nickname"] = data["data"][str(account_id)]["nickname"]
                                print(ign_data)
                                return ign_data

        def PostIGNError(self,group_id,chat_id):
                message = "[BOTより返信]\nIGNにマッチしたデータが見つかりませんでした\n再度IGN入力してください"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostAskOK(self,group_id,chat_id,battles,nickname):
                message = "[BOTより返信]\n検索結果を表示します\nIGN："+ nickname + "\n戦闘数：" + str(battles) + "\n間違いがなければこのメッセージにグーをしてください\n違っていればブーを押してください\n再度IGNを入力できます"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostWhichClan(self,group_id,chat_id):
                message = "[BOTより返信]\n所属したいクランの希望を聞きます\n以下の表に従って数字（半角）を返信してください\nWWN：1\nWWN-2：2\nWWN-3：3\nWWN-4：4\nWWN-E：5\nどれでも：6\n\n"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostClanNumberError(self,group_id,chat_id):
                message = "[BOTより返信]\n番号の入力が不適切です\n半角で1～6のいづれかを再度返信してください"
                response = self.PostReply(group_id,chat_id,message)
                return response
        def PostStartExam(self,group_id,chat_id,admin_room_id,ign_data,clan):
                message = "[BOTより返信]\n担当者が審査を開始します\n（この作業には最大数日かかる可能性があります）\n審査ののち担当者がロビーで個チャをいたします\nしばらくお待ちください"
                response = self.PostReply(group_id,chat_id,message)
                lobi_url = "https://web.lobi.co/game/world_of_tanks_blitz/group/" + str(group_id) + "/chat/" + str(chat_id)
                blitz_star_url = "https://www.blitzstars.com/player/asia/" + ign_data["nickname"]
                message = "[BOTより送信]\n広報室より入隊希望の" + ign_data["nickname"] + "さん\n" + lobi_url + "\n基本情報は以下の通りです\n\nIGN：" + ign_data["nickname"] + "\n戦闘数：" + str(ign_data["battles"]) + "\n勝率：" + str(ign_data["winrate"]) + "\n最終戦闘日：" + str(ign_data["last_battle_time"]) + "\n所属希望：" + clan + "\n" + blitz_star_url + "\n\n戦闘名声、ツイッターの確認お願いします\n以後の作業は司令官に引き継ぎます"
                response = self.PostMessage(admin_room_id,message)
                return response["id"]

if __name__ == "__main__":
        api = RecruitingBot()
        api.Login("taiseimaruyama7171@gmail.com", "maru0807171")
        application_id = "eda85c3d6ddbb56920d3544319a4a788"
        api.UpdateAccessToken(application_id)
