import datetime
import pytz
import json
from common import *
from bs4 import BeautifulSoup
import os


# 讀課表資料
def getjsonCourseData():
    with open(os.path.join('data', 'courseData.json') ,encoding='utf-8') as f:
        jsonCourseData = json.load(f)
    return jsonCourseData

#獲取今日課表資料
def getTodayCourse(jsonCourseData):
    timezoneTW = pytz.timezone('Asia/Taipei')
    idxTodayWeekday = datetime.datetime.now(timezoneTW).weekday()
    return getDayCourse(jsonCourseData,idxTodayWeekday)


# 獲取指定日期課表資料
def getDayCourse(jsonCourseData,intWeekDay):
    
    listDayCourse = []
    for i in range(len(jsonCourseData)):
        if jsonCourseData[i]['星期']==weekdayMapping[intWeekDay]:
            listDayCourse.append(jsonCourseData[i])
    if listDayCourse is not None:
        return listDayCourse
    else:
        return None
    
#下一個有課日
def getNextCourseDay():
    jsonCourseData = getjsonCourseData()
    timezoneTW = pytz.timezone('Asia/Taipei')
    idxToday = datetime.datetime.now(timezoneTW).weekday()
    for i in range(idxToday+1,idxToday+8):
        i = i%7
        if getDayCourse(jsonCourseData,i):
            return i
    return None

# 取得距離現在時間最接近的節次
def getNextPeriodNearNow(strTimeCurrent):
    strTimeCurrent = strTimeCurrent.strftime('%H:%M')  # 將現在時間轉換為字串格式，僅保留時分
    dictSortedPeriods = sorted(dictMappingPeriodTime.items(), key=lambda x: x[1])  # 將節次開始時間排序
    lenPeriods = len(dictSortedPeriods)
    
    for i in range(lenPeriods):
        periodCode, periodTime = dictSortedPeriods[i]
        nextPeriodCode, nextPeriodTime = dictSortedPeriods[(i + 1) % dictSortedPeriods]  # 循環遍歷節次列表
        if periodTime > strTimeCurrent:
            return periodCode, periodTime
        elif nextPeriodTime <= strTimeCurrent < periodTime:  # 處理超過最後一個節次的情況
            return nextPeriodCode, nextPeriodTime
    return None, None  # 如果沒有找到下一個節次，則返回 None


# 取得下一堂課
def getNextCourse(jsonCourseData, timeCurrent):
    # 取得今天的課程
    todayCourses = getTodayCourse(jsonCourseData)
    
    # 如果今天有課程
    if len(todayCourses)!=0:
        # 找到下一個節次的課程
        nextCourse = getNextPeriodCourse(todayCourses, timeCurrent)
        if nextCourse:
            return nextCourse
    
    # 如果今天沒有課程或找不到下一個節次的課程，從明天開始找下一堂課
    nextCourseDay = getNextCourseDay()
    if nextCourseDay is not None:
        nextDayCoureSchedule = getDayCourse(jsonCourseData, nextCourseDay)
        if len(nextDayCoureSchedule):
            return nextDayCoureSchedule[0]
    
    # 如果明天也沒有課程，返回 None
    return None

# 取得同天中，距離現在最近的下一堂課
def getNextPeriodCourse(todayCourses, timeCurrent):
    timeCurrentStr = timeCurrent.strftime('%H:%M')
    nextCourse = None
    minTimeDiff = float('inf')  # 初始設置一個極大值來存放最小時間差
    for course in todayCourses:
        courseTime = dictMappingPeriodTime.get(course['節次'].split('-')[0])  # 取得課程開始時間
        if courseTime:
            timeDiff = (datetime.datetime.strptime(courseTime, '%H:%M') - datetime.datetime.strptime(timeCurrentStr, '%H:%M')).total_seconds()
            # 如果時間差為負，表示課程已經開始，不考慮這個課程
            if timeDiff >= 0 and timeDiff < minTimeDiff:
                minTimeDiff = timeDiff
                nextCourse = course
    return nextCourse




def getScheduleData():
    data = getjsonCourseData()
    
    scheduleData = []

    # 對所有可能的星期進行處理
    for day in ["一", "二", "三", "四", "五", "六"]:
        # 初始化該天的課程列表
        daySchedule = (day, [])
        
        for course in data:
            if course["星期"] == day and course["節次"] != "-":
                time = course["節次"]
                courseName = course["科目名稱"]
                
                # 將節次的格式轉換為所需格式
                if "-" in time:
                    start, end = time.split("-")
                    start = periodMapping[start]
                    end = periodMapping[end]
                    timeRange = f"{start}-{end}"
                else:
                    timeRange = periodMapping[int(time)]
                
                # 將課程添加到該天的課程列表中
                daySchedule[1].append((timeRange, courseName))
        
        # 添加該天的課程列表到 scheduleData 中
        scheduleData.append(daySchedule)
    return scheduleData


def mergeSameRowHtml(htmlContent):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(htmlContent, 'html.parser')
    trs = soup.find_all('tr')[1:]
    # 遍歷每一列，合併相同的儲存格
    for i in range(6):  
        rowSpan = 1
        for j in range(len(trs)):
            tds = trs[j].find_all('td')
            # 檢查該列中是否存在第 i 列的儲存格
            if len(tds) > i:
                currentCell = tds[i]
                for k in range(j + 1, len(trs)):
                    nextTds = trs[k].find_all('td')
                    # 檢查下一行的第 i 列是否存在並與當前儲存格的值相同
                    if len(nextTds) > i and nextTds[i].get_text() == currentCell.get_text() :
                        # 將下一行的相同儲存格標記為待刪除
                        nextTds[i]['kill'] = '1'
                        rowSpan += 1
                        currentCell['rowspan'] = rowSpan
                    else:
                        rowSpan = 1
                        break
                    
    # 刪除所有有屬性 'kill'='1' 的標籤
    for tag in soup.find_all(attrs={"kill": "1"}):
        tag.decompose()
    # 將修改後的 HTML 內容轉換為字串
    modifiedHtml = soup.prettify()
    return modifiedHtml



            

            