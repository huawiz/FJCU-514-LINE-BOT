# FJU Line Bot 

# 功能
- [ ] 最新消息
- [x]課表選單
  - [x] 下一節課
  - [x] 更新課表
  - [x] 課表表格(WebView)
  - [ ] 圖片顯示

- [ ] 登入功能
  - [ ] 資料庫
  - [ ] LIFF
  - [ ] Access Token機制
  
# 輸入模式

使用Line Bot輸入指令，Line API會透過網頁傳送Post至Flask服務。

# 輸出模式

Flask收到Post指令後，處理完對應任務後，透過Line Message API回傳，並顯示在Line Bot。

# Python語法應用

# 程式碼資訊

## 環境
`後端語言`:Python 3.11
`Module`:
```
line-bot-sdk
flask
pytz
lxml
bs4
requests
python-dotenv
```
`Host平台`: Azure Web Services

## 命名規則

Camel Case


## 檔案用途切分

``` 
│  
├─data
│     └─courseData.json
│      
└─templates
│     └─course.html
├─.env
├─app.py
├─common.py
├─coursedata.py
├─LineMessage.py
├─scraper.py
└─requirements.txt     
```


# 更新歷程

2024/5/21 完成初版，包含課表選單、下一節課、課表(WebView)