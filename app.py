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
dict = {}    # {"WATCHWORD":"URL"}

HIRAGANA_LIST = list(u"あいうえおかきくけこさしすせそたちつてと"\
                  u"なにぬねのはひふへほまみむめもやゆよ"\
                  u"らりるれろわをん")

users = {}



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
    return "REX THE LIVE!!!"




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
    with open('data/data.json','r') as f:
        dict = json.load(f)

    tmp = dict

    # 暗号と照合..................
    ww = event.message.text
    flag = False
    dlfile = ""
    for t in dict:
        if dict[t]['PW'] == ww:
            dlfile = t
            flag = True

    if flag:
        messages = []
        messages.append(TextSendMessage(text='SUCCESS'))
        # result = dbx.files_get_temporary_link('/SHARE/' + dict[ww])
        # m = TextSendMessage(text=str(result))
        # messages.append(m)

        # url = 'https://github.com/yu-ig/ezbt'
        vm = VideoSendMessage(
            original_content_url="https://damp-sands-30274.herokuapp.com/static/"+t,
            preview_image_url="https://damp-sands-30274.herokuapp.com/static/0.jpg"
        )
        messages.append(vm)

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
 JSON add id  [id, DL, PW]
'''
@app.route('/post/<string:post_text>')
def post(post_text):
    # show the post with the given id, the id is an integer
    t = post_text.split(',')

    f = open("data/data.json", mode='r')
    json_data = json.load(f)

    # ココ重要！！
    # インデントありで表示
    # print("{}".format(json.dumps(json_data, indent=4)))
    f.close()

    with open("data/data.json", 'w') as f2:
        '''
        ここでjsonに加筆
        
        '''
        json_data[t[0]] = {
            "DL": t[1],
            "PW": t[2]
        }

        f2.write(str(json.dumps(json_data, indent=4)))

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    dbx.users_get_current_account()
    dbx.files_download_to_file(t[0]+'.mp4', 'static/' + t[0]+'.mp4')


    return str(t[0]+" "+t[1] + " " +t[2])


# @app.route('/post/<string:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     t = post_id.split(',')
#
#     w =""
#     for tmp in t :
#         w += tmp
#
#     return w

@app.route('/get/')
def getJson():
    f = open("data/data.json", mode='r')
    json_data = json.load(f)
    return json.dumps(json_data)


@app.route('/getDebug/')
def getDebug():
    f = open("data/data.json", mode='r')
    json_data = json.load(f)
    tmp = ""
    for t in json_data:
        tmp += json_data[t]['PW'] + " "

    return tmp


# 文字列を適当に生成するよ。
def generateWW(length):
    watchword = ""
    for i in range(length):
        n = len(HIRAGANA_LIST)
        watchword = watchword + HIRAGANA_LIST[random.randint(0, n-1)]

    return watchword



def dbx():
    print("Initializing Dropbox API...")
    dbx = dropbox.Dropbox("4c0XTxvPmbAAAAAAAABrXqips-_F7J8hZ6LCMsVgRb4uKZEr08Mvf-VMv1b8mupE")
    dbx.users_get_current_account()
    # f = open(filePath, 'rb')
    # filename = str(datetime.datetime.now()) + ".mp4"
    # dbx.files_upload(f.read(), '/SHARE/' + filename)
    # f.close()

    # metadata, f = dbx.files_download('/' + j)
    # out = open(j, 'wb')
    # out.write(f.content)
    # out.close()





if __name__ == "__main__":
    # 環境変数をゲット　なければセット　
    # post(1,"000000", "jijsdiaji")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)






# {
#     "type": "video",
#     "originalContentUrl": "https://example.com/original.mp4",
#     "previewImageUrl": "https://example.com/preview.jpg"
# }