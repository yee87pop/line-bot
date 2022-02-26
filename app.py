from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage, ImageSendMessage
)
import configparser

import os
import psycopg2
import learnSomething
import weather
import json
import requests
import random
import string
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    
    signature = request.headers['X-Line-Signature']

    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if ('學習/' in event.message.text) and (not('//' in event.message.text)):
        QandA=event.message.text.split('/')
        try:
            print(QandA)
            learnSomething.input_Q(QandA[1],QandA[2])
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我學會了!!"))       
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我聽不懂"))
    elif '明天天氣' in event.message.text :
        try:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=weather.weather_search(event.message.text[0]+event.message.text[1]+event.message.text[2])))           
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有這個地方喔"))
    else:
        try:
            print(event.message.text)
            ans=learnSomething.output_A(event.message.text)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ans))   
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="聽無")) 

@handler.add(MessageEvent, message=ImageMessage)
def handle_message2(event):
    try:
        image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
        image_content = line_bot_api.get_message_content(event.message.id)
        image_name = image_name.upper()+'.jpg'
        path='./static/'+image_name
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
        original_content_url='https://www.greenpeace.org/static/planet4-hongkong-stateless/2019/10/90e80dbb-penguin-chick.jpg',
        preview_image_url='https://upload.wikimedia.org/wikipedia/commons/c/cd/Chinstrap_Penguin.jpg'
        ))        
    except:
        print('error')
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="error"))

    
if __name__ == "__main__":
    app.run()


