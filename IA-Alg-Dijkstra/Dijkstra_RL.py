# ------------------------------------
#      Dijkstra para la vida real
#    Encontrar el camino mas rapido 
# ------------------------------------

import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
#      Algoritmo de Dijkstra 
# -----------------------------
def dijkstra(graph, start):
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
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
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return distances, previous

def shortest_path(previous, start, end):
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    return path if path[0] == start else []

# ---------------------------------------------------------
# CASO DE LA VIDA REAL: RUTA AL TRABAJO CON TRÁFICO (DATA)
# ---------------------------------------------------------
# Los valores representan el TIEMPO EN MINUTOS para cruzar esa calle.
# "Arrojar un resultado entre la data" significa que el algoritmo
# encontrará la ruta de menor tiempo en este conjunto de datos.
mapa_trafico = {
    "Oficina": {"Av_Principal": 10, "Calle_Lateral": 5},
    "Av_Principal": {"Glorieta": 15, "Puente_Norte": 8},
    "Calle_Lateral": {"Glorieta": 12, "Zona_Residencial": 20},
    "Glorieta": {"Puente_Norte": 5, "Casa": 10},
    "Puente_Norte": {"Casa": 4},
    "Zona_Residencial": {"Casa": 2},
    "Casa": {}
}

# Definimos origen y destino
punto_partida = "Oficina"
punto_llegada = "Casa"

# Ejecutamos el algoritmo
tiempos, historial = dijkstra(mapa_trafico, punto_partida)
mejor_ruta = shortest_path(historial, punto_partida, punto_llegada)

# -----------------------------
# RESULTADOS "ARROJADOS"
# -----------------------------
print(f"--- SISTEMA DE NAVEGACIÓN INTELIGENTE ---")
print(f"Buscando la ruta más rápida desde {punto_partida}...")
print(f"Tiempo estimado de llegada: {tiempos[punto_llegada]} minutos.")
print(f"Ruta sugerida: {' -> '.join(mejor_ruta)}")

# -----------------------------
# GRAFICAR EL MAPA DE LA CIUDAD
# -----------------------------
G = nx.DiGraph()
for nodo in mapa_trafico:
    for vecino, peso in mapa_trafico[nodo].items():
        G.add_edge(nodo, vecino, weight=peso)

# Usamos un layout que se vea más como un mapa (shell o planar)
pos = nx.shell_layout(G)

plt.figure(figsize=(10, 7))
nx.draw_networkx_nodes(G, pos, node_color="#2ecc71", node_size=3000)
nx.draw_networkx_edges(G, pos, edge_color="gray", arrowstyle='->', arrowsize=20, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight="bold")

# Etiquetas de minutos (la data de tráfico)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

# Resaltar la ruta óptima en ROJO
if len(mejor_ruta) > 1:
    ruta_aristas = list(zip(mejor_ruta, mejor_ruta[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=ruta_aristas, edge_color="red", width=3, arrowstyle='->', arrowsize=30)

plt.title(f"Optimización de Ruta: {punto_partida} a {punto_llegada}\n(Los números azules son minutos de tráfico)", fontsize=14)
plt.axis("off")
plt.show()