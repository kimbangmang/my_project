import requests
year = 2021
month = 1
for month in range(10):
    print(month)
# while month <= 11:
#     month = month + 1
#     print(month)
leagueCode = 'lck_2021_spring'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = f'https://sports.news.naver.com/esports/schedule/monthly.nhn?date=20210220&year={year}&month={str(month).zfill(2)}&leagueCode={leagueCode}&category=lol'
print(url)
data = requests.get(url, headers=headers)
result = data.json() # json 데이터를 파이썬에서 다룰 수 있게 변환
# 전체 json data
# print(result)
monthlyScheduleDailyGroup = result['monthlyScheduleDailyGroup']
# print(month)
for dailyGroup in monthlyScheduleDailyGroup:
    # print(dailyGroup)
    scheduleList = dailyGroup['scheduleList']
    # print(scheduleList)
    for schedule in scheduleList:
        gameDate = (schedule['gameStartDate'])
        homeTeamName = (schedule['homeTeamName'])
        awayTeamName = (schedule['awayTeamName'])
        homeTeamScore = (schedule['homeTeamScore'])
        awayTeamScore = (schedule['awayTeamScore'])
        print(gameDate, homeTeamName,homeTeamScore, awayTeamName, awayTeamScore)

