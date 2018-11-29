
import random
import dropbox
import requests

import json

users = {}
dict = {"01": "/SHARE/00.mp4"}



HIRAGANA_LIST = list(u"あいうえおかきくけこさしすせそたちつてと"\
                  u"なにぬねのはひふへほまみむめもやゆよ"\
                  u"らりるれろわをん")

DROPBOX_APP_KEY = "eqdo0y9azq27imf"
DROPBOX_APP_SECRET = "1k04vbqlsuxv4dt"
DROPBOX_ACCESS_TOKEN = "4c0XTxvPmbAAAAAAAABrzS3I8NhjijADE7JPcUGZ2ycMO9K4yyQflLkoahUF5JNR"

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


def generateWW(length):
    watchword = ""
    for i in range(length):
        n = len(HIRAGANA_LIST)
        watchword = watchword + HIRAGANA_LIST[random.randint(0, n-1)]

    return watchword

if __name__ == "__main__":
    # #l = list(NAMES_CHARS)
    # metadata, f = dbx.files_download(dict["01"])
    # result = dbx.files_get_temporary_link(dict["01"])
    # # out = open(dict["01"], 'wb')
    # data = f.content
    # # out.close()
    # out = open('00.mp4', 'wb')
    # out.write(f.content)
    # out.close()
    # print("result "+str(result))
    # print("::: "+str(out))
    # print(len(data), 'bytes; md:', metadata)
    #
    # s = generateWW(10)
    # # print(s)
    requests.get("https://damp-sands-30274.herokuapp.com/post/000002,kkfkkfkd,lsdd")
    print("FINISH")

