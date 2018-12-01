import dropbox
import time
import os
import json
#
DROPBOX_APP_KEY = "eqdo0y9azq27imf"
DROPBOX_APP_SECRET = "1k04vbqlsuxv4dt"
DROPBOX_ACCESS_TOKEN = "4c0XTxvPmbAAAAAAAABrzS3I8NhjijADE7JPcUGZ2ycMO9K4yyQflLkoahUF5JNR"

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))



if __name__ == "__main__":
    f = open("../data/data.json", mode='r')
    json_data = json.load(f)

    # ココ重要！！
    # インデントありで表示
    # print("{}".format(json.dumps(json_data, indent=4)))
    f.close()

    lis = []
    ks = json_data.keys()
    for k in ks:
        lis.append(k)
        print(k)
    print(str(lis[0]))
    # show the post with the given id, the id is an integer
    path = "/SHARE/"+lis[0]
    md, res = dbx.files_download(path)
    out = open("../static/"+lis[0], 'wb')
    out.write(res.content)
    out.close()

