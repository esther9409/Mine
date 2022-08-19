from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import re
import datetime
import time
import math
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# def index(request):
#     return HttpResponse("My First Django App.")

# @csrf_exempt
# def callback(request):
 
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')
 
#         try:
#             events = parser.parse(body, signature)  # 傳入的事件
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
 
#         for event in events:
#             if isinstance(event, MessageEvent):  # 如果有訊息事件
#                 line_bot_api.reply_message(  # 回復傳入的訊息文字
#                     event.reply_token,
#                     TextSendMessage(text=event.message.text)
#                 )
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()


callback = ['汪','汪汪','汪汪汪']

@csrf_exempt
def back(request):

	if request.method == 'POST':
		signature = request.META['HTTP_X_LINE_SIGNATURE']
		body = request.body.decode('utf-8')

		try:
			events = parser.parse(body, signature)
		except InvalidSignatureError:
			return HttpResponseForbidden()
		except LineBotApiError:
			return HttpResponseBadRequest()

		for event in events:
			if isinstance(event, MessageEvent):
				if '設定提醒' in event.message.text:
					content = event.message.text.split(' ')
					now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").split(' ')
					now_date = now[0].split('-')
					now_time = now[1].split(':')
					date_user = content[1].split('-')
					time_user = content[2].split(':')
					temp_now = datetime.datetime(int(now_date[0]),int(now_date[1]),int(now_date[2]),int(now_time[0]),int(now_time[1]))
					temp_user = datetime.datetime(int(date_user[0]),int(date_user[1]),int(date_user[2]),int(time_user[0]),int(time_user[1]))
					if temp_now < temp_user:
						clock = str(temp_user-temp_now).split(' ')
						if 'days' in clock:
							days = int(clock[0])
							hours = int(clock[2].split(':')[0])
							mins = int(clock[2].split(':')[1])
						else:
							days = 0
							hours = int(clock[0].split(':')[0])
							mins = int(clock[0].split(':')[1])
						try:
							tmp_id = event.source.group_id
						except:
							tmp_id = event.source.user_id
						time.sleep((days*24*60*60)+(hours*60*60)+(mins*60))
						line_bot_api.push_message(
							tmp_id,
							TextSendMessage(text=content[3])
						)
					elif temp_now == temp_user:
						line_bot_api.reply_message(
							event.reply_token,
							TextSendMessage(text=content[3])
						)
					else:
						line_bot_api.reply_message(
							event.reply_token,
							TextSendMessage(text=content[1]+'已過 無法設定提醒')
						)
				elif '設定推播' in event.message.text:
					content = event.message.text.split(' ')
					try:
						tmp_id = event.source.group_id
					except:
						tmp_id = event.source.user_id
					if content[2] == 'H' or content[2] == 'h':
						during = int(content[1])*60
					elif content[2] == 'M' or content[2] == 'm':
						during = int(content[1])
					interval = int(content[3])
					num = 0
					while num <= during:
						line_bot_api.push_message(
							tmp_id,
							TextSendMessage(text=content[4])
						)
						num += interval
						time.sleep(interval*60)
				# elif '多多' in event.message.text or '阿胖' in event.message.text or '阿肥' in event.message.text:
				# 	line_bot_api.reply_message(
				# 		event.reply_token,
				# 		TextSendMessage(text=random.choice(callback))
				# 	)
				elif '屎' in event.message.text:
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text='罰錢')
					)
				elif '仔仔' in event.message.text or '胖仔' in event.message.text or '臭仔' in event.message.text:
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text=random.choice(callback))
					)
				elif '握手' in event.message.text or '左手' in event.message.text or '右手' in event.message.text:
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text='汪(舉手')
					)
				elif '坐下' in event.message.text:
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text='汪')
					)
				elif re.match(r'汪+', event.message.text):
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text=event.message.text+'汪')
					)
				else:
					line_bot_api.reply_message(
						event.reply_token,
						TextSendMessage(text='汪?')
					)
		return HttpResponse()
	else:
		return HttpResponseBadRequest()
