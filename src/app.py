from flask import Flask, request, abort
import os
from command import webhookHandler,handleMessage
from coursedata import renderCourse
from map import renderMap
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# flask服務
app = Flask(__name__)

# Render WebView 課表
@app.route('/course')
def course():
    render = renderCourse()
    return render


# Render WebView 課表
@app.route('/map')
def map():
    render = renderMap()
    return render


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        webhookHandler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 指令動作
@webhookHandler.add(MessageEvent, message=TextMessage)
def webhookHandleMessage(event):
    handleMessage(event)
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
