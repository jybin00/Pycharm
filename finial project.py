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


def num(graph, start_node):
    visit = list()
    stack = list()
    articulation_point = set()
    num_value = dict()
    low_value = dict()
    parent = dict()
    counter = 0

    stack.append(start_node)

    while stack:
        node = stack.pop()
        if node not in visit:
            counter = counter + 1
            visit.extend(node)
            num_value[node] = counter
            stack.extend(graph[node])

    for low_val in graph:
        low_value[low_val] = num_value.get(low_val)
    for k, value in graph.items():
        for val in value:
            if num_value.get(val) > num_value.get(k):
                if low_value.get(val) >= num_value.get(k):
                    articulation_point.add(k)
                low_value[k] = min(low_value.get(k), low_value.get(val))
            else:
                if num_value.get(k) > num_value.get(val):
                    low_value[k] = min(low_value.get(k), num_value.get(val))

    return num_value, low_value, articulation_point


x, y, z = num(graph1, 'A')
print("Original graph")
print()

for key, value in graph1.items():
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





