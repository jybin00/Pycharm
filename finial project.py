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

from queue import Queue

graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'D', 'H'],
         'D': ['B', 'C'],
         'E': ['F', 'G'],
         'F': ['E', 'G'],
         'G': ['E', 'F'],
         'H': ['C', 'I', 'J'],
         'I': ['H', 'J'],
         'J': ['H', 'I']}


# def bfs(graph, start_node):
#     visit = list()
#     q = Queue()
#
#     q.put(start_node)
#
#     while q.qsize() > 0:
#         node = q.get()
#         if node not in visit:
#             visit.append(node)
#             for nextNode in graph[node]:
#                 q.put(nextNode)
#     return visit


def articulation(graph, start_node):
    visit = list()
    stack = list()
    low = list()
    counter = 0

    stack.append(start_node)

    while stack:
        node = stack.pop()
        if node not in visit:
            counter = counter + 1
            visit.extend([node, counter])
            stack.extend(graph[node])

    return visit


# def AssignNum(graph, start_node):
#     num = list()
#     visited = list()
#     counter = 0
#
#     num[node] = counter++
#     visited[node] = Ture


print("Original graph")
print()

for key, value in graph.items():
    print(key, ":", value)
print()
print("Num value\n")
for i in range(0, len(articulation(graph, 'A')), 2):
    print(articulation(graph, 'A')[i:i+2])


