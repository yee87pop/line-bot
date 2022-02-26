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

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
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
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
        original_content_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.greenpeace.org%2Fhongkong%2Fissues%2Fclimate%2Fupdate%2F11868%2F%25E6%25B0%25A3%25E5%2580%2599%25E5%258D%25B1%25E6%25A9%259F%25E4%25BB%25A4%25E6%25B5%25B7%25E5%2586%25B0%25E8%259E%258D%25E5%258C%2596-%25E5%258D%2597%25E6%25A5%25B5%25E7%259A%2587%25E5%25B8%259D%25E4%25BC%2581%25E9%25B5%259D%25E3%2580%258C%25E5%2586%2587%25E6%258E%259F%25E4%25BC%2581%25E3%2580%258D%25E6%2588%2596%25E6%2588%2590%2F&psig=AOvVaw2cZfhQzlRUaj21OYoa0C4t&ust=1645940876393000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKCZpNzVnPYCFQAAAAAdAAAAABAD',
        preview_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fzh.wikipedia.org%2Fwiki%2F%25E4%25BC%2581%25E9%25B5%259D&psig=AOvVaw0MmCg4Z34984Zp8bQjYQKO&ust=1645940901244000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLjK7efVnPYCFQAAAAAdAAAAABAD'
        ))        
    except:
        print('error')
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="error"))

    
if __name__ == "__main__":
    app.run()


