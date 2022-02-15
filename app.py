from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import configparser

import os
import psycopg2
import learnSomething

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
    if '學習/' in event.message.text:
        QandA=event.message.text.split('/')
        try:
            learnSomething.input_Q(QandA[1],QandA[2])
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我學會了!!"))            
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(event.message.text))
    else:
        try:
            ans=learnSomething.output_A(event.message.text)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ans))   
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="傻逼~")) 


    
if __name__ == "__main__":
    app.run()


