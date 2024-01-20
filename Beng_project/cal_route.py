from flask import Flask, request, jsonify
import networkx as nx
from collections import deque
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)


def haversine(coord1, coord2):
    # 지구의 반경 (킬로미터 단위)
    R = 6371.0

    # 좌표에서 위도 및 경도 추출
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # 위도 및 경도 간의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine 공식 적용
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c

    return distance

def read_coordinates_from_file(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            lat, lon = map(float, value.split(','))
            coordinates[key] = (lat, lon)
    return coordinates

def create_graph(coordinates):
    graph = nx.Graph()
    
    for key1, coord1 in coordinates.items():
        for key2, coord2 in coordinates.items():
            if key1 != key2:
                distance = haversine(coord1, coord2)
                graph.add_edge(key1, key2, weight=distance)
    
    return graph

def dijkstra(graph, start, end):
    path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    total_distance = nx.shortest_path_length(graph, source=start, target=end, weight='weight')
    return path, total_distance

def bfs(graph, start, end):
    path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    total_distance = nx.shortest_path_length(graph, source=start, target=end, weight='weight')
    return path, total_distance

# 루트 경로에 대한 처리
@app.route('/')
def index():
    return "Hello, this is the root page!"

# 파일 경로
file_path = "1RCoordinate.txt"


# 좌표 정보 읽어오기
coordinates = read_coordinates_from_file(file_path)

# 그래프 생성
graph = create_graph(coordinates)

# Recommend Path 엔드포인트
@app.route('/recommend_path', methods=['POST'])
def recommend_path():
    data = request.get_json()
    start_node = data['start']
    end_node = data['end']

    # 다익스트라 알고리즘을 통한 경로 추천
    path_dijkstra, total_distance_dijkstra = dijkstra(graph, start_node, end_node)

    # 너비 우선 탐색 알고리즘을 통한 경로 추천
    path_bfs, total_distance_bfs = bfs(graph, start_node, end_node)

    response = {
        'dijkstra': {
            'path': path_dijkstra,
            'total_distance': total_distance_dijkstra
        },
        'bfs': {
            'path': path_bfs,
            'total_distance': total_distance_bfs
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)