import coursedata
import json
def msgNextClass():
    msg ='''
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "@[#星期幾#]@",
                "size": "xs",
                "color": "#000000",
                "align": "center",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#FF6B6B",
            "paddingStart": "4px",
            "cornerRadius": "100px",
            "position": "relative",
            "paddingEnd": "4px",
            "paddingAll": "2px",
            "width": "70px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "@[#教室#]@",
                "size": "xs",
                "color": "#000000",
                "align": "center",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#F4A261",
            "paddingStart": "4px",
            "cornerRadius": "100px",
            "position": "relative",
            "paddingEnd": "4px",
            "paddingAll": "2px",
            "width": "70px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "@[#節次#]@",
                "size": "xs",
                "color": "#000000",
                "align": "center",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#7DCE82",
            "paddingStart": "4px",
            "cornerRadius": "100px",
            "position": "relative",
            "paddingEnd": "4px",
            "paddingAll": "2px",
            "width": "70px"
          }
        ],
        "spacing": "5px"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "contents": [],
                "size": "xl",
                "wrap": true,
                "text": "@[#課程名稱#]@",
                "color": "#ffffff",
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "@[#授課教師#]@",
                "color": "#ffffffcc",
                "size": "sm"
              }
            ],
            "spacing": "sm"
          }
        ],
        "offsetTop": "5px",
        "margin": "3px"
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#292F36"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "@[#開課單位#]@",
                "color": "#000000",
                "size": "xs",
                "align": "start"
              },
              {
                "type": "text",
                "text": "@[#課程代碼#]@",
                "align": "end",
                "color": "#000000",
                "size": "xs"
              }
            ]
          }
        ],
        "paddingStart": "8px",
        "spacing": "5px"
      }
    ],
    "backgroundColor": "#FFFFFF"
  }
}
'''
    CourseData = coursedata.getjsonCourseData()
    tw = coursedata.pytz.timezone('Asia/Taipei')
    currentTime = coursedata.datetime.datetime.now(tw)
    nextCourse = coursedata.getNextCourse(CourseData,currentTime)
    msg = msg.replace('@[#課程名稱#]@',nextCourse['科目名稱'])
    msg = msg.replace('@[#授課教師#]@',nextCourse['授課教師'])
    msg = msg.replace('@[#星期幾#]@','週'+nextCourse['星期'])
    msg = msg.replace('@[#教室#]@',nextCourse['教室'])
    msg = msg.replace('@[#節次#]@',nextCourse['節次'])
    msg = msg.replace('@[#開課單位#]@',nextCourse['開課單位名稱'])
    msg = msg.replace('@[#課程代碼#]@',nextCourse['課程代碼'])
    return json.loads(msg)

def msgNextClassText():
    CourseData = coursedata.getjsonCourseData()
    tw = coursedata.pytz.timezone('Asia/Taipei')
    currentTime = coursedata.datetime.datetime.now(tw)
    nextCourse = coursedata.getNextCourse(CourseData,currentTime)
    return f"{nextCourse['科目名稱']}/{nextCourse['教室']}/{nextCourse['星期']}/{nextCourse['節次']}"
    

def msgCourseMenu():
    msg = '''
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "contents": [],
        "size": "xl",
        "wrap": true,
        "text": "課表功能",
        "color": "#ffffff",
        "weight": "bold"
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#292F36"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "下一節課",
              "text": "下一節課"
            },
            "style": "secondary",
            "margin": "none"
          },
          {
            "type": "separator",
            "margin": "md"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "全部課表",
              "uri": "https://hualinebot.azurewebsites.net/course"
            },
            "style": "secondary"
          }
        ]
      }
    ],
    "backgroundColor": "#FFFFFF"
  }
}
    '''
    return json.loads(msg)

def defaultAction():
    msg = '''
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "contents": [],
        "size": "xl",
        "wrap": true,
        "text": "? ",
        "color": "#ffffff",
        "weight": "bold"
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#292F36"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "課表",
              "text": "課表選單"
            },
            "style": "secondary",
            "margin": "none"
          },
          {
            "type": "separator",
            "margin": "md",
            "color": "#ffffff"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "更新課表",
              "text": "更新課表"
            },
            "style": "secondary"
          }
        ]
      }
    ],
    "backgroundColor": "#FFFFFF"
  }
}
    '''
    return json.loads(msg)