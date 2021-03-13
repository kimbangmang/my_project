import requests
from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse

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
            gameTime = (schedule['gameStartTime'])
            homeTeamName = (schedule['homeTeamName'])
            awayTeamName = (schedule['awayTeamName'])
            homeTeamScore = (schedule['homeTeamScore'])
            awayTeamScore = (schedule['awayTeamScore'])

            doc = {
                'gameDate': gameDate,
                'gameTime': gameTime,
                'homeTeamName': homeTeamName,
                'awayTeamName': awayTeamName,
                'homeTeamScore': homeTeamScore,
                'awayTeamScore': awayTeamScore,
            }
            result.append(doc)
            print(gameDate, homeTeamName, homeTeamScore, awayTeamName, awayTeamScore)
    print(result)
    return jsonify({'result': 'success', 'data': result})



@app.route('/api/rank', methods=['GET']) # 팀 순위 보여주기
def rank_get():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
    data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bjFE&pkid=475&os=17568053&qvt=0&query=2021%20LoL%20%EC%B1%94%ED%94%BC%EC%96%B8%EC%8A%A4%20%EC%BD%94%EB%A6%AC%EC%95%84%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%A0%95%EA%B7%9C%EC%88%9C%EC%9C%84', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ranking_chart = soup.select('#main_pack > div.sc_new.cs_common_module.case_normal._kgs_esports.color_7 > div.cm_content_wrap > div > div > div > div > div > div > table > tbody > tr')
    result = []

    for ranking_chart in ranking_chart:
        a = ranking_chart.select_one('td > span')
        if a is not None:
            number = a.text[0:2].strip()
            teamName = ranking_chart.select_one('a > span').text
            win = ranking_chart.select_one('td:nth-child(2) > span').text.strip()
            loss = ranking_chart.select_one('td:nth-child(3) > span').text.strip()
            winningRate = ranking_chart.select_one('td:nth-child(4) > span').text.strip()
            point = ranking_chart.select_one('td:nth-child(5) > span').text.strip()

            doc = {
                'number': number,
                'teamName': teamName,
                'win': win,
                'loss': loss,
                'winningRate': winningRate,
                'point': point,

            }

            result.append(doc)
            print(number, teamName, win, loss, winningRate, point)
    print(result)
    return jsonify({'result': 'success', 'data': result})

@app.route('/api/highlight', methods=['GET']) # 유튜브 하이라이트 영상 보여주기
def highlight_get():
    # extract playlist id from url
    url = 'https://www.youtube.com/playlist?list=PLIWtfvmBcNofWeZRz8xxz9ZzVpgocF8rR'
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    print(f'get all playlist items links from {playlist_id}')
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyAVDRkjd0KCHFUr5eZJuZXXs1TfG26hxIQ")

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    print(f"total: {len(playlist_items)}")
    print([
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
        for t in playlist_items
    ])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)