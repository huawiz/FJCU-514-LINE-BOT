from flask import Flask, request, abort,render_template
import os
import scraper
from common import *
from coursedata import *
import LineMessage
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()


# Channel Access Token
line_bot_api = LineBotApi(os.getenv('Channel_Access_Token'))


# Channel Secret
handler = WebhookHandler(os.getenv('Channel_Secret_Token'))


@app.route('/course')
def course():
    # 課表資料
    scheduleData=getScheduleData()
    periodMapping = {'D0': 0,'D1': 1,'D2': 2,'D3': 3,'D4': 4,'DN': 5,'D5': 6,'D6': 7,'D7': 8,'D8': 9,'E0': 10,'E1': 11,'E2': 12,'E3': 13,'E4': 14}
    # render網頁，並合併表格
    render = mergeSameRowHtml(render_template('course.html',**locals()))
    return render

# 監聽所有來自 /callback 的 Post Request，Line API使用
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

# 訊息反應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mesg = event.message.text
    if mesg == '下一節課':
        try:
            message = FlexSendMessage(LineMessage.msgNextClassText(),LineMessage.msgNextClass())
            line_bot_api.reply_message(event.reply_token, message)
        except:
            message = TextSendMessage(text='資料異常，請嘗試更新課表')
            line_bot_api.reply_message(event.reply_token, message)
    elif mesg == '更新課表':
        try:
            scraper.updateCourse(os.getenv('StuAccount'),os.getenv('StuPassword'))
            message = TextSendMessage(text='更新完成')
            line_bot_api.reply_message(event.reply_token, message)
        except:
            message = TextSendMessage(text='更新異常')
            line_bot_api.reply_message(event.reply_token, message)

    elif mesg == '課表選單':
        message = FlexSendMessage('課表功能',LineMessage.msgCourseMenu())
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = FlexSendMessage('?',LineMessage.defaultAction())
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
