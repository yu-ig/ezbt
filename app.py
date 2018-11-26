from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, VideoMessage, TextSendMessage, VideoSendMessage
)
import logging
import os
import dropbox
import random
import json
import urllib3

# 合言葉 dictionary
dict = {"vid": "00.mp4"}    # {"WATCHWORD":"URL"}

HIRAGANA_LIST = list(u"あいうえおかきくけこさしすせそたちつてと"\
                  u"なにぬねのはひふへほまみむめもやゆよ"\
                  u"らりるれろわをん")



CHANNEL_SECRET = "73b66d519d69ee046316e77735e6e0a4"
CHANNEL_ACCESS_TOKEN = "s+twVpc3vWjdE5t0A1yozYeboN3xytQyb+eVJr3yAmsvYiQoxyaR2MsnBkru5J1mwXIrCR2z128PXC6OLKtTrUtpC9FwZrlLfrEdWF/9vAsXa1N26aUB2BU58OiCzAyCqtMJlOPzZNwO5j69+Sx9rAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask("__name__")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)



DROPBOX_APP_KEY = "eqdo0y9azq27imf"
DROPBOX_APP_SECRET = "1k04vbqlsuxv4dt"
DROPBOX_ACCESS_TOKEN = "4c0XTxvPmbAAAAAAAABrzS3I8NhjijADE7JPcUGZ2ycMO9K4yyQflLkoahUF5JNR"

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


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


@handler.add(MessageEvent, message=VideoMessage)
def handle_message(event):
    # 暗号と照合..................
    ww = event.message.text
    if ww in dict.keys():
        # l = list(NAMES_CHARS)
        # metadata, f = dbx.files_download('/SHARE/'+dict[ww])
        # result = dbx.files_get_temporary_link('/SHARE/'+dict[ww])
        # out = open(dict["01"], 'wb')
        # data = f.content
        # out.close()
        # out = open(dict[ww], 'wb')
        # out.write(f.content)
        # out.close()
        # print("::: " + str(data))
        # print(len(data), 'bytes; md:', metadata)
        # if watchword  dict
        url = 'https://damp-sands-30274.herokuapp.com/send/'
        path = '00.mp4'
        mojiretsu = "mojimojimoji"
        line_bot_api.reply_message(
            event.reply_token,
            # TextSendMessage(text='SUCCESS!! ' + url+path)

            VideoSendMessage(
                original_content_url='https://www.dropbox.com/s/beqlhwn4y8szbcr/00.mp4?dl=0'
                # preview_image_url='https://example.com/preview.jpg'
            )
            #TextSendMessage(text=event.message.text)
        )
        # os.remove(out)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text + "?\n合言葉が違うよ。")
        )


'''
 JSON add id
'''
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id




# 文字列を適当に生成するよ。
def generateWW(length):
    watchword = ""
    for i in range(length):
        n = len(HIRAGANA_LIST)
        watchword = watchword + HIRAGANA_LIST[random.randint(0, n-1)]

    return watchword


if __name__ == "__main__":
    # 環境変数をゲット　なければセット　
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)






# {
#     "type": "video",
#     "originalContentUrl": "https://example.com/original.mp4",
#     "previewImageUrl": "https://example.com/preview.jpg"
# }