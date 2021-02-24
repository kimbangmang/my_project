import requests

url_1 = 'https://sports.news.naver.com/esports/schedule/scoreboard.nhn?date='
url_2 = '&year=2021&leagueCode=lck_2021_spring&month=02&category=lol'
date = '20210101'
data = requests.get
# result = data.json() # json 데이터를 파이썬에서 다룰 수 있게 변환


for i in range(10):
    url_full = url_1 + date + url_2
    date1 = (int(date) + 1)
    print(url_full)