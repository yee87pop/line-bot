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

app = Flask(__name__)

line_bot_api = LineBotApi('ni5XsV3T4QI9NMpivwVNMktrHt04BupNGb0gjiLoHVo6pwK6qOTOUoD4swDhvk6CsmV/QS9XmRG3wxl8sa+mIPUFMx+zOD/7pM1Z1309aCHAe/B/oQTKxJrwNSTQsXaNq/dTUXUbY/Jd1RedYfCTZAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('14bfb8f1e55ca21fc9f5b4d5c241642f')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()