import os
import base64
import requests
import json
from PIL import ImageGrab
import win32clipboard as w
import win32con
#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py
#
env = os.environ
default_headers = {
    "content-type": "application/json",
    "app_id": "my-id",
    "app_key": "my-key"
}
service = 'https://api.mathpix.com/v3/text'
#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()
#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)
#
# 识别并将公式latex返回剪切板
#
def setText(aString): # 向剪贴板发送字符串
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def mathpix_clipboard(): # 识别剪贴板公式
    im = ImageGrab.grabclipboard()
    im.save('equa.png','PNG')
    r = latex({
        'src': image_uri("equa.png")
    })
    result = r['text']
    setText(result[2:-2])

if __name__ == '__main__':
    mathpix_clipboard()