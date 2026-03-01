import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Dijkstra con reconstrucción de camino
# -----------------------------
def dijkstra(graph, start):
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0

    # Para reconstruir el camino
    previous = {node: None for node in graph}

    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node  # Guardamos por dónde llegamos
                heapq.heappush(queue, (distance, neighbor))

    return distances, previous


# -----------------------------
# Función para reconstruir el camino más corto
# -----------------------------
def shortest_path(previous, start, end):
    path = []
    current = end

    while current is not None:
        path.insert(0, current)
        current = previous[current]

    if path[0] == start:
        return path
    else:
        return []  # No hay camino


# -----------------------------
# Grafo ya definido por ti
# -----------------------------
graph = {
    "A": {"B": 4, "C": 3, "D":2},
    "B": {"C": 5, "D": 10, "E": 8},
    "C": {"D": 3, "E": 6},
    "D": {"E": 6},
    "E": {}
}

# -----------------------------
# Ejecutar Dijkstra desde un nodo inicial
# -----------------------------
start_node = "A"
end_node = "E"  # <- El nodo al que quieres encontrar la ruta más rápida

distances, previous = dijkstra(graph, start_node)

print("Distancias más cortas desde:", start_node)
for node, distance in distances.items():
    print(f"{node}: {distance}")

# -----------------------------
# Obtener el camino más corto hacia end_node
# -----------------------------
best_path = shortest_path(previous, start_node, end_node)
print("\nRuta más rápida de", start_node, "a", end_node, ": ", best_path)


# -----------------------------
# GRAFICAR EL GRAFO
# -----------------------------
G = nx.DiGraph()

# Agregar nodos y aristas
for nodo in graph:
    for vecino, peso in graph[nodo].items():
        G.add_edge(nodo, vecino, weight=peso)

# Layout automático
pos = nx.spring_layout(G, seed=42)


# Dibujar nodos
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2000)

# Dibujar TODAS las aristas (azules)
nx.draw_networkx_edges(G, pos, edge_color="blue", arrowstyle='->', arrowsize=25)

# Dibujar etiquetas de nodos
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

# Dibujar pesos de aristas
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# -----------------------------
# Resaltar la ruta más rápida (en ROJO)
# -----------------------------
if len(best_path) > 1:
    best_edges = list(zip(best_path, best_path[1:]))

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=best_edges,
        edge_color="red",
        width=2,
        arrowstyle='->',
        arrowsize=25
    )

plt.title("Grafo con Ruta Más Corta en Rojo")
plt.axis("off")
plt.show()
