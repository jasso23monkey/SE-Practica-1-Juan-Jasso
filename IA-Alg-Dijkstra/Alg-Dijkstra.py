import sys
import heapq

def dijkstra(graph, start):
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        distancia, Nodo = heapq.heappop(queue)

        if distancia > distances[Nodo]:
            continue

        for neighbor, weight in graph[Nodo].items():
            distance = distancia + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

graph = {}

numVertices = int(input("Ingrese el numero de vertices de Grafo: "))

for i in range(numVertices):
    vertex = input(f"Ingrese el vertice {i+1}: ")
    edges = {}

    while True:
        edge = input("Ingrese el adyacente (o fin para terminar): ")

        if edge == 'fin':
            break

        weight = float(input("Ingrese el peso de la arista: "))
        edges[edge] = weight

    graph[vertex] = edges

startNodo = input("Ingrese el Nodo Inicial: ")

distances = dijkstra(graph, startNodo)

print("Distancias mas cortas desde el nodo inicial: ")
for node, distance in distances.items():
    print(f"Nodo: {node}, Distancia: {distance}")
