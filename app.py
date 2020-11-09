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

line_bot_api = LineBotApi('hpwj9cmUMM7fcQD+7InEvDx4tAY5pWMPIyEVDTYKulnSmV6nVbYZAqSnLtBz/Q/le6cnNmuPgjkq+XHk6dCQ4JPdfjhblIWdkle5EIHjT5wWtGRhJ2r7+MX6E5MvoPGrVG3MimKK0LqCKxOIWdSZgAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4d748cc7935f4b03317ec3e9f67f498d')


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