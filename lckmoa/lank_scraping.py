import requests
year = 2021
month = 2
leagueCode = 'lck_2021_spring'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = f'https://sports.news.naver.com/esports/schedule/monthly.nhn?date=20210220&year={year}&month={str(month).zfill(2)}&leagueCode={leagueCode}&category=lol'
print(url)
data = requests.get(url, headers=headers)
result = data.json() # json 데이터를 파이썬에서 다룰 수 있게 변환
# 전체 json data
# print(result)
monthlyScheduleDailyGroup = result['monthlyScheduleDailyGroup']

for dailyGroup in monthlyScheduleDailyGroup:
    schedule = dailyGroup['scheduleList']
    print(schedule)


# 숫자를 더해 날짜 변경하는 방식으로 했는데 31까지 한 후, 01이면 02로 넘어가고 다시 1일부터 계산하는 법 알아보기
# LCK말고 다른 리그도 결과에 나오는데 LCK리그만 불러오도록 하기