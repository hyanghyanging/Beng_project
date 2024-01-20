import requests
import json

url = 'http://127.0.0.1:5000/recommend_path'  # Flask 애플리케이션의 주소로 변경하세요

# POST 요청에 사용할 데이터 (출발지와 목적지를 설정)
data = {
    'start': 'CENTER',
    'end': 'TOP_LEFT'
}

# JSON 형식으로 데이터를 전송
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

# 응답 결과 확인
if response.status_code == 200:
    result = response.json()
    print("Dijkstra Algorithm:", result['dijkstra'])
    print("BFS Algorithm:", result['bfs'])
else:
    print("Error:", response.status_code, response.text)
