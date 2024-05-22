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

# 處理訊息
def handleMessage(event):
    message = event.message.text

    handlers = {
        '下一節課': handleNextClass,
        '更新課表': handleUpdateCourse,
        '課表選單': handleCourseMenu,
        '學校地圖':handleMap
    }

    webhookHandler = handlers.get(message, handleDefault)
    webhookHandler(event)

# 指令:下一節課
def handleNextClass(event):
    try:
        message = FlexSendMessage(LineMessage.msgNextClassText(), LineMessage.msgNextClass())
        linebotAPI.reply_message(event.reply_token, message)
    except Exception as e:
        print(f"Error handling '下一節課': {e}")
        message = TextSendMessage(text='資料異常，請嘗試更新課表')
        linebotAPI.reply_message(event.reply_token, message)

# 指令:更新課表
def handleUpdateCourse(event):
    try:
        scraper.updateCourse(os.getenv('StuAccount'), os.getenv('StuPassword'))
        message = TextSendMessage(text='更新完成')
        linebotAPI.reply_message(event.reply_token, message)
    except Exception as e:
        print(f"Error updating course: {e}")
        message = TextSendMessage(text='更新異常')
        linebotAPI.reply_message(event.reply_token, message)

# 指令:課表選單
def handleCourseMenu(event):
    message = FlexSendMessage('課表功能', LineMessage.msgCourseMenu())
    linebotAPI.reply_message(event.reply_token, message)


# 指令:預設(任何訊息)
def handleDefault(event):
    message = FlexSendMessage('?', LineMessage.defaultAction())
    linebotAPI.reply_message(event.reply_token, message)


def handleMap(event):
    message = TextSendMessage(text='https://hualinebot.azurewebsites.net/map')
    linebotAPI.reply_message(event.reply_token, message)
