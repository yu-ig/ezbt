from flask import Flask, request, abort, render_template, send_file, Response, stream_with_context

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
    # result = dbx.sharing_get_shared_link_file('https://www.dropbox.com/home/%E3%82%A2%E3%83%97%E3%83%AA/LDH/SHARE/00.mp4')
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
    # 暗号と照合..................
    ww = event.message.text
    if ww in dict.keys():
        messages = []


        messages.append(TextSendMessage(text='https://www.youtube.com/watch?v=IC-wDpwzEt4 '))
        # result = dbx.files_get_temporary_link('/SHARE/' + dict[ww])
        # m = TextSendMessage(text=str(result))
        # messages.append(m)

        # url = 'https://github.com/yu-ig/ezbt'
        # vm = VideoSendMessage(
        #     original_content_url="https://damp-sands-30274.herokuapp.com/send/00.mp4",
        #     preview_image_url="https://damp-sands-30274.herokuapp.com/send/0.jpg"
        # )
        # messages.append(vm)

        ###############################################################
        line_bot_api.reply_message(
            event.reply_token,
            messages
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
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/report1/<string:report_id>', methods=['GET'])
def report1(report_id):

    # ★ポイント2
    downloadFileName = 'report1_' + 00 + '.mp4'
    downloadFile = 'send/00.mp4'

    # ★ポイント3
    return send_file(downloadFile, as_attachment = True, mimetype = 'video/mp4')




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