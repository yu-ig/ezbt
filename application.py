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
import urllib
import glob2


application = Flask(__name__)


CHANNEL_SECRET = "b62983e501542254d522c7ab6472ee53"
CHANNEL_ACCESS_TOKEN = "4CfX8hrXiTkamU1tz2xI/G3wbHbpN9qegFJxBs6+/1LVnXgF/a/qMLoyIqMeq89IwXIrCR2z128PXC6OLKtTrUtpC9FwZrlLfrEdWF/9vAttETQ6CaDSzJoKXsjOj76i8ad0DUqd8R1pCNGbtJitygdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


DROPBOX_APP_KEY = "eqdo0y9azq27imf"
DROPBOX_APP_SECRET = "1k04vbqlsuxv4dt"
DROPBOX_ACCESS_TOKEN = "4c0XTxvPmbAAAAAAAABrzS3I8NhjijADE7JPcUGZ2ycMO9K4yyQflLkoahUF5JNR"

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)





@application.route("/")
def index():

    return "Hello world"



@application.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    application.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # with open('data/data.json','r') as f:
    #     dict = json.load(f)
    #
    # tmp = dict
    #
    # # 暗号と照合..................
    # ww = event.message.text
    # flag = False
    dlfile = ""
    # for t in dict:
    #     if dict[t]['PW'] == ww:
    #         dlfile = t
    #         flag = True
    #
    # if flag:
    #     messages = []
    #     messages.append(TextSendMessage(text='SUCCESS'))
    #     # result = dbx.files_get_temporary_link('/SHARE/' + dict[ww])
    #     # m = TextSendMessage(text=str(result))
    #     # messages.append(m)
    #
    #
    #     # url = 'https://github.com/yu-ig/ezbt'
    #     vm = VideoSendMessage(
    #         original_content_url="https://damp-sands-30274.herokuapp.com/static/"+dlfile,
    #         preview_image_url="https://damp-sands-30274.herokuapp.com/static/0.jpg"
    #     )
    #     # messages.append(vm)
    #
    #     ###############################################################
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         messages
    #     )
    #     # os.remove(out)
    #
    # else:
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=event.message.text + "?\n合言葉が違うよ。")
    #     )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="SUCCESS!!")
    )



@application.route('/get/')
def getJson():
    f = open("data/data.json", mode='r')
    json_data = json.load(f)

    # ココ重要！！
    # インデントありで表示
    # print("{}".format(json.dumps(json_data, indent=4)))
    f.close()
    for t in json_data:
        path = "/SHARE/" + t
        md, res = dbx.files_download(path)
        out = open("static/" + t, 'wb')
        out.write(res.content)

    return json.dumps(json_data)



@application.route('/post/<string:post_text>')
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

    path = "/SHARE/"+t[0]
    md, res = dbx.files_download(path)
    out = open("static/"+t[0], 'wb')
    out.write(res.content)
    out.close()



    return str(t[0]+" "+t[1] + " " +t[2])



@application.route('/getDebug/')
def getDebug():
    f = open("data/data.json", mode='r')
    json_data = json.load(f)

    # ココ重要！！
    # インデントありで表示
    # print("{}".format(json.dumps(json_data, indent=4)))
    f.close()
    # for t in json_data:
    #     path = "/SHARE/" + t
    #     md, res = dbx.files_download(path)
    #     out = open("static/" + t, 'wb')
    #     out.write(res.content)
    tmp = ""
    for t in json_data:
        tmp += json_data[t]['PW'] + " "

    return tmp

@application.route('/getFiles/')
def getFiles():
    fs = glob2.glob("static/*.mp4")
    t = ""
    for f in fs:
        t += f + "\n"

    return t


if __name__ == "__main__":
    application.debug = True
    application.run()
