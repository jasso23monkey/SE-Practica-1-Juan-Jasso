import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------
# Simulador del Árbol Parcial Mínimo (APM)
# usando el algoritmo de Prim, con salida
# paso a paso en consola y gráfica con
# networkx + matplotlib.
# -------------------------------------------

def prim_mst(graph, start):
    """
    Implementación básica del algoritmo de Prim.

    Parámetros:
        graph: dict de dicts
            Ejemplo:
            {
                "A": {"B": 2, "C": 3},
                "B": {"A": 2, "C": 1, "D": 4},
                ...
            }
        start: nodo inicial (string)

    Regresa:
        mst_edges: lista de tuplas (u, v, w) -> aristas del APM
        total_cost: costo total del APM
    """

    visited = set([start])
    mst_edges = []
    total_cost = 0
    step = 1

    print("\n====== SIMULADOR PRIM - PASO A PASO ======")
    print(f"Nodo inicial: {start}")
    print("------------------------------------------")

    while len(visited) < len(graph):
        best_edge = None  # (u, v, w)

        # Buscar la mejor arista (más barata) que conecte
        # un nodo visitado con uno no visitado
        for u in visited:
            for v, w in graph[u].items():
                if v not in visited:
                    if best_edge is None or w < best_edge[2]:
                        best_edge = (u, v, w)

        if best_edge is None:
            print("El grafo NO es completamente conectable desde el nodo inicial.")
            break

        u, v, w = best_edge
        visited.add(v)
        mst_edges.append(best_edge)
        total_cost += w

        print(f"\nPaso {step}:")
        print(f"  Arista elegida: {u} -- {v} (peso {w})")
        print(f"  Nodo agregado al árbol: {v}")
        print(f"  Nodos en el árbol ahora: {sorted(list(visited))}")
        print(f"  Costo acumulado: {total_cost}")
        print("------------------------------------------")

        step += 1

    print("\n====== RESULTADO FINAL DEL APM (PRIM) ======")
    print("Aristas del Árbol Parcial Mínimo:")
    for (u, v, w) in mst_edges:
        print(f"  {u} -- {v} (peso {w})")
    print(f"Costo total del árbol: {total_cost}")

    return mst_edges, total_cost


def mostrar_grafo(graph):
    """
    Imprime el grafo de manera amigable en consola.
    """
    print("Grafo (nodo: vecinos(peso)):")
    for u, vecinos in graph.items():
        conexiones = ", ".join(f"{v}({w})" for v, w in vecinos.items())
        print(f"  {u} -> {conexiones}")


def crear_grafo_ejemplo():
    """
    Crea un grafo de ejemplo para probar el algoritmo.
    Puedes modificar este grafo para tus pruebas.
    Debe ser NO dirigido (simétrico).
    """
    graph = {
        "A": {"B": 2, "C": 3},
        "B": {"A": 2, "C": 1, "D": 4, "E": 5},
        "C": {"A": 3, "B": 1, "D": 3},
        "D": {"B": 4, "C": 3, "E": 1},
        "E": {"B": 5, "D": 1}
    }
    return graph


# ----------- PARTE GRÁFICA (NETWORKX) ----------------

def construir_grafo_networkx(graph):
    """
    Convierte el diccionario 'graph' en un grafo de networkx.
    """
    G = nx.Graph()
    # Agregar nodos y aristas con pesos
    for u, vecinos in graph.items():
        for v, w in vecinos.items():
            # Para evitar agregar dos veces la misma arista en grafo no dirigido
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=w)
    return G


def dibujar_grafo_y_mst(graph, mst_edges):
    """
    Dibuja el grafo completo y resalta el Árbol Parcial Mínimo (mst_edges).
    """
    G = construir_grafo_networkx(graph)

    # Posiciones de los nodos (puedes cambiar el layout si quieres)
    pos = nx.spring_layout(G, seed=42)  # layout "bonito" automático

    # --- Dibujar nodos ---
    nx.draw_networkx_nodes(G, pos, node_size=800)

    # --- Dibujar todas las aristas en gris ---
    nx.draw_networkx_edges(G, pos, width=2, edge_color="lightgray")

    # --- Etiquetas de nodos ---
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    # --- Etiquetas de pesos de TODAS las aristas ---
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    # --- Resaltar las aristas del MST ---
    # mst_edges viene como lista de (u, v, w)
    mst_edge_list = [(u, v) for (u, v, w) in mst_edges]

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=mst_edge_list,
        width=3,
        edge_color="red"
    )

    plt.title("Árbol Parcial Mínimo (Prim)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ----------------- MAIN ---------------------

def main():
    # 1. Crear o cargar el grafo
    graph = crear_grafo_ejemplo()

    print("==========================================")
    print("   SIMULADOR ÁRBOL PARCIAL MÍNIMO (PRIM)  ")
    print("==========================================\n")

    # 2. Mostrar el grafo en consola
    mostrar_grafo(graph)
    print()

    # 3. Pedir nodo inicial
    nodos = list(graph.keys())
    print(f"Nodos disponibles: {nodos}")
    start = input("Elige nodo inicial para Prim (por defecto A): ").strip()

    if start == "" or start not in graph:
        print("Nodo inválido, se usará 'A' por defecto.")
        start = "A"

    # 4. Ejecutar Prim (con pasos en consola)
    mst_edges, total_cost = prim_mst(graph, start)

    # 5. Dibujar el grafo y el MST
    #    (si el grafo no era conectable, mst_edges podría estar vacío)
    if mst_edges:
        dibujar_grafo_y_mst(graph, mst_edges)
    else:
        print("No se pudo construir el MST, no se dibuja la gráfica.")

    print("\nFin de la simulación.\n")


if __name__ == "__main__":
    main()
