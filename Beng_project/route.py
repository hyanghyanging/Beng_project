from flask import Flask, render_template, request, jsonify
import heapq
from haversine import haversine

app = Flask(__name__)

def read_coordinates_from_file(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            lat, lon = map(float, value.split(','))
            coordinates[key] = (lat, lon)
    return coordinates

def calculate_distance(coord1, coord2):
    return haversine(coord1, coord2)

def dijkstra(graph, start, end):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_node = end
    while current_node != start:
        path.insert(0, current_node)
        current_node = distances[current_node][1]

    path.insert(0, start)

    return path, distances[end]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_shortest_path', methods=['POST'])
def find_shortest_path():
    data = request.get_json()

    # 파일 경로를 입력으로 받습니다.
    file_path = "1RCoordinate.txt"
    
    # 파일에서 좌표 정보를 읽어옵니다.
    coordinates = read_coordinates_from_file(file_path)

    # 그래프를 생성합니다.
    graph = {}
    for key1, coord1 in coordinates.items():
        graph[key1] = {}
        for key2, coord2 in coordinates.items():
            if key1 != key2:
                distance = calculate_distance(coord1, coord2)
                graph[key1][key2] = distance

    # 출발지와 목적지를 설정합니다.
    start_node = data['start']
    end_node = data['end']

    # 다익스트라 알고리즘을 실행합니다.
    path, total_distance = dijkstra(graph, start_node, end_node)

    # 결과를 JSON 형식으로 반환합니다.
    response = {
        'path': path,
        'total_distance': total_distance
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
