from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, VideoSendMessage
)
import logging
import os


# 合言葉 dictionary
dict = {'hi':"おめでとう。"}    # {"id":"URL"}


CHANNEL_SECRET = "73b66d519d69ee046316e77735e6e0a4"
CHANNEL_ACCESS_TOKEN = "s+twVpc3vWjdE5t0A1yozYeboN3xytQyb+eVJr3yAmsvYiQoxyaR2MsnBkru5J1mwXIrCR2z128PXC6OLKtTrUtpC9FwZrlLfrEdWF/9vAsXa1N26aUB2BU58OiCzAyCqtMJlOPzZNwO5j69+Sx9rAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask("__name__")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)



@app.route('/')
def index():
    return "Hello world"



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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ww = event.message.text
    if ww in dict.keys():
        # if watchword  dict
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='SUCCESS!!' + dict[ww])

            # VideoSendMessage(
            #     original_content_url=dict[ww],
            #     preview_image_url='https://example.com/preview.jpg'
            # )
            #TextSendMessage(text=event.message.text)
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text + "?\n合言葉が違うよ。")
        )






if __name__ == "__main__":
    # 環境変数をゲット　なければセット　
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)






{
    "type": "video",
    "originalContentUrl": "https://example.com/original.mp4",
    "previewImageUrl": "https://example.com/preview.jpg"
}