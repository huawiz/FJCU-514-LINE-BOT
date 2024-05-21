from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
import os
import scraper
from dotenv import load_dotenv
import LineMessage

load_dotenv()
# Channel Access Token
linebotAPI = LineBotApi(os.getenv('Channel_Access_Token'))
# Channel Secret
webhookHandler = WebhookHandler(os.getenv('Channel_Secret_Token'))



def handleNextClass(event):
    try:
        message = FlexSendMessage(LineMessage.msgNextClassText(), LineMessage.msgNextClass())
        linebotAPI.reply_message(event.reply_token, message)
    except Exception as e:
        print(f"Error handling '下一節課': {e}")
        message = TextSendMessage(text='資料異常，請嘗試更新課表')
        linebotAPI.reply_message(event.reply_token, message)

def handleUpdateCourse(event):
    try:
        scraper.updateCourse(os.getenv('StuAccount'), os.getenv('StuPassword'))
        message = TextSendMessage(text='更新完成')
        linebotAPI.reply_message(event.reply_token, message)
    except Exception as e:
        print(f"Error updating course: {e}")
        message = TextSendMessage(text='更新異常')
        linebotAPI.reply_message(event.reply_token, message)

def handleCourseMenu(event):
    message = FlexSendMessage('課表功能', LineMessage.msgCourseMenu())
    linebotAPI.reply_message(event.reply_token, message)

def handleDefault(event):
    message = FlexSendMessage('?', LineMessage.defaultAction())
    linebotAPI.reply_message(event.reply_token, message)

@webhookHandler.add(MessageEvent, message=TextMessage)
def handleMessage(event):
    message = event.message.text

    handlers = {
        '下一節課': handleNextClass,
        '更新課表': handleUpdateCourse,
        '課表選單': handleCourseMenu
    }

    webhookHandler = handlers.get(message, handleDefault)
    webhookHandler(event)