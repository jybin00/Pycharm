# Goal: Finding articulation points in a graph
# •  Input:  three different connected undirected graphs with vertices >= 10 and A.Ps >= 3
# • Algorithm sketches are given in the textbook and slides
#
#
# • Output: For each graph, print
#
#
# –Original graph
#
#
# –Num values of all vertices
#
#
# –Low values of all vertices
#
#
# –All the articulation points and extra information to show how your
# program can find out those articulation points.

# 알아야되는 개념 :
# DFS -> 깊이 우선 탐색(은 preorder의 일반화로 볼 수 있다.) Biconnected graph -> 어느 한 노드가 끊어져도
# 원래 그래프와 연결되면 biconnected graph라고 함. 그렇지 않은 그래프는 articulation point를 가지고 있음.
# Num(v) -> preorder number
# Low(v) -> 다시 돌아올 수 있는 노드의 Num(v)


# undirected graph


graph1 = {'A': ['B', 'C'],
          'B': ['A', 'D', 'E'],
          'C': ['A', 'D', 'H'],
          'D': ['B', 'C'],
          'E': ['B', 'F', 'G'],
          'F': ['E', 'G'],
          'G': ['E', 'F'],
          'H': ['C', 'I', 'J'],
          'I': ['H', 'J'],
          'J': ['H', 'I']}


graph2 = {'A': ['B', 'C'],
          'B': ['A', 'C', 'D'],
          'C': ['A', 'B', 'G'],
          'D': ['B', 'E'],
          'E': ['D', 'F'],
          'F': ['E'],
          'G': ['C', 'I'],
          'H': ['I'],
          'I': ['G', 'H', 'J'],
          'J': ['I']}

graph3 = {'A': ['B'],
          'B': ['A', 'C', 'K'],
          'C': ['B', 'G', 'D'],
          'D': ['C', 'E', 'I'],
          'E': ['D', 'F', 'H'],
          'F': ['E'],
          'G': ['C'],
          'H': ['D', 'E'],
          'I': ['D', 'J'],
          'J': ['I'],
          'K': ['B']}


def num(graph, start_node):  # ariculation 포인트를 찾는 함수
    visit = list()  # 방문한 곳을 기록하는 스택
    stack = list()  # 반복 작업을 위한 스택
    articulation_point = set()  # 단절점을 저장하는 집합
    num_value = dict()  # num 값을 저장하는 딕셔너리
    low_value = dict()  # low 값을 저장하는 딕셔너리
    counter = 0  # num 값용 카운터

    stack.append(start_node)  # 시작점 스택에 넣기

    while stack:
        node = stack.pop()  # 스택에 있는 요소 꺼내기
        if node not in visit:  # 노드에 방문한 적이 없으면
            counter = counter + 1
            visit.extend(node)  # 방문한 노드에 넣기
            num_value[node] = counter  # num값 넣기
            stack.extend(graph[node])  # 방문한 노드 주변 노드 가져오기

    for low_val in graph:  # 모든 그래프 노드에 대해
        low_value[low_val] = num_value.get(low_val)  # 자신의 num값을 low값으로 초기화
    for k, value in graph.items():  # 그래프에 있는 key값과 value값에 대해
        for val in value:  # 하나의 키 안에 있는 value 값을 가져와서
            if num_value.get(val) > num_value.get(k):  # 만약에 주변 노드의 num값이 키의 num보다 크면
                if low_value.get(val) >= num_value.get(k):  # 만약 주변 노드의 low값이 키의 num보다 크면
                    articulation_point.add(k)  # articulation point
                low_value[k] = min(low_value.get(k), low_value.get(val))
            else:
                if num_value.get(k) > num_value.get(val): # 만약 역방향이면 즉, 값이 작아지는 방향
                    low_value[k] = min(low_value.get(k), num_value.get(val)) # 키의 low와 주변의 num의 미니멈

    return num_value, low_value, articulation_point


def articulation(graph):  # 결과를 표현하기 위한 함수
    x, y, z = num(graph, 'C')
    print("Original graph")
    print()

    for key, value in graph.items():
        print(key, ":", value)
    print()

    print("Num value\n")
    for i, item in x.items():
        print(i, ":", item)
    print()

    print("Low value\n")
    for j, item in y.items():
        print(j, ":", item)
    print()

    print("articulation points are", z)


articulation(graph1)

articulation(graph2)

articulation(graph3)





