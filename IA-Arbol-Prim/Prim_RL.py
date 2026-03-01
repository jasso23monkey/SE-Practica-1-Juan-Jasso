# ---------------------------------------------------------
#                    Arbol minimo de PRIM 
#              Algoritmo para Sistema de Riego
# ---------------------------------------------------------

import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------
#                       FUNCIÓN PRIM 
# ---------------------------------------------------------
def prim_mst(graph, start):
    visited = set([start])
    mst_edges = []
    total_cost = 0
    step = 1

    print("\n====== OPTIMIZANDO DISEÑO DE RIEGO - PASO A PASO ======")
    print(f"Punto de inicio (Bomba/Estanque): {start}")
    print("-------------------------------------------------------")

    while len(visited) < len(graph):
        best_edge = None 
        for u in visited:
            for v, w in graph[u].items():
                if v not in visited:
                    if best_edge is None or w < best_edge[2]:
                        best_edge = (u, v, w)

        if best_edge is None:
            break

        u, v, w = best_edge
        visited.add(v)
        mst_edges.append(best_edge)
        total_cost += w

        print(f"Paso {step}: Conectando {u} con {v}")
        print(f"  Longitud de tubería: {w} metros.")
        print(f"  Metros totales acumulados: {total_cost}m")
        print("-------------------------------------------------------")
        step += 1

    print("\n====== RESULTADO FINAL DE LA RED DE RIEGO ======")
    print(f"Metros totales de tubería requeridos: {total_cost}m")
    return mst_edges, total_cost

# ---------------------------------------------------------
# CASO DE LA VIDA REAL: RED DE RIEGO AGRÍCOLA (DATA)
# ---------------------------------------------------------
def crear_sistema_riego():
    # Los nodos son zonas de una granja
    # Los pesos son la distancia en metros entre ellas
    red_riego = {
        "Estanque_Principal": {"Invernadero": 15, "Huerto_Frutales": 25, "Zona_Siembra": 10},
        "Invernadero": {"Estanque_Principal": 15, "Huerto_Frutales": 10, "Almacen": 30},
        "Huerto_Frutales": {"Estanque_Principal": 25, "Invernadero": 10, "Caballerizas": 20},
        "Zona_Siembra": {"Estanque_Principal": 10, "Almacen": 12},
        "Almacen": {"Zona_Siembra": 12, "Invernadero": 30, "Caballerizas": 15},
        "Caballerizas": {"Huerto_Frutales": 20, "Almacen": 15}
    }
    return red_riego

# ----------- PARTE GRÁFICA ADAPTADA ----------------

def dibujar_riego(graph, mst_edges):
    G = nx.Graph()
    for u, vecinos in graph.items():
        for v, w in vecinos.items():
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))

    # Dibujar nodos (Zonas del campo)
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="#3498db")
    
    # Dibujar todas las conexiones posibles en gris (Caminos posibles)
    nx.draw_networkx_edges(G, pos, width=1, edge_color="lightgray", style="--")

    # Resaltar la RED DE RIEGO ÓPTIMA en AZUL FUERTE (Tubería instalada)
    mst_edge_list = [(u, v) for (u, v, w) in mst_edges]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edge_list, width=4, edge_color="#1f3a93")

    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Mapa de Instalación de Tubería (Mínimo Material Requerido)", fontsize=14)
    plt.axis("off")
    plt.show()

# ----------------- EJECUCIÓN ---------------------

def main():
    mapa_granja = crear_sistema_riego()
    
    # Punto de partida: El Estanque donde está la bomba de agua
    punto_inicio = "Estanque_Principal"
    
    # Ejecutar Prim
    tuberias_finales, metros_totales = prim_mst(mapa_granja, punto_inicio)

    # Mostrar visualmente
    dibujar_riego(mapa_granja, tuberias_finales)

if __name__ == "__main__":
    main()