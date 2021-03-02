import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/games', methods=['GET']) # 월별 경기 정보 보여주기
def test_get():
    year = request.args.get('year_give', 2021)
    month = request.args.get('month_give', 1)
    leagueCode = 'lck_2021_spring'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = f'https://sports.news.naver.com/esports/schedule/monthly.nhn?date=20210220&year={year}&month={str(month).zfill(2)}&leagueCode={leagueCode}&category=lol'
    print(url)
    data = requests.get(url, headers=headers)
    result = data.json()  # json 데이터를 파이썬에서 다룰 수 있게 변환
    monthlyScheduleDailyGroup = result['monthlyScheduleDailyGroup']
    result = []
    for dailyGroup in monthlyScheduleDailyGroup:
        scheduleList = dailyGroup['scheduleList']
        for schedule in scheduleList:
            gameDate = (schedule['gameStartDate'])
            homeTeamName = (schedule['homeTeamName'])
            awayTeamName = (schedule['awayTeamName'])
            homeTeamScore = (schedule['homeTeamScore'])
            awayTeamScore = (schedule['awayTeamScore'])
            doc = {
                'gameDate': gameDate,
                'homeTeamName': homeTeamName,
                'awayTeamName': awayTeamName,
                'homeTeamScore': homeTeamScore,
                'awayTeamScore': awayTeamScore
            }
            result.append(doc)
            print(gameDate, homeTeamName, homeTeamScore, awayTeamName, awayTeamScore)
    print(result)
    return jsonify({'result': 'success', 'data': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)