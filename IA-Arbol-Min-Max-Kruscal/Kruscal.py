import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------
# Simulador Árbol de MÍNIMO y MÁXIMO coste
# usando el algoritmo de Kruskal.
#
# - Muestra paso a paso en consola.
# - Dibuja el grafo y resalta el árbol encontrado.
# -------------------------------------------

# ======= ESTRUCTURAS AUXILIARES (UNION-FIND) =======

class UnionFind:
    """
    Estructura de conjuntos disjuntos (Union-Find)
    para detectar ciclos de forma eficiente.
    """
    def __init__(self, elementos):
        # Cada elemento es su propio padre al inicio
        self.parent = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}

    def find(self, x):
        # Encuentra el representante del conjunto de x (con compresión de caminos)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Une los conjuntos de x e y por rango
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False  # ya estaban en el mismo conjunto (formaría ciclo)

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

        return True  # unión exitosa, no ciclo


# ======= LÓGICA DE KRUSKAL =======

def kruskal(edges, modo="minimo"):
    """
    Algoritmo de Kruskal.

    Parámetros:
        edges: lista de aristas (u, v, w)
            u, v: nodos
            w: peso (costo)
        modo: "minimo" o "maximo"

    Regresa:
        tree_edges: lista de aristas seleccionadas
        total_cost: suma de pesos del árbol
    """

    # 1. Obtener lista de nodos
    nodos = set()
    for (u, v, w) in edges:
        nodos.add(u)
        nodos.add(v)

    # 2. Ordenar las aristas según el modo
    if modo == "minimo":
        edges_ordenadas = sorted(edges, key=lambda x: x[2])      # menor a mayor
        print("\n=== KRUSKAL - ÁRBOL DE MÍNIMO COSTE ===")
    else:
        edges_ordenadas = sorted(edges, key=lambda x: x[2], reverse=True)  # mayor a menor
        print("\n=== KRUSKAL - ÁRBOL DE MÁXIMO COSTE ===")

    uf = UnionFind(nodos)
    tree_edges = []
    total_cost = 0
    step = 1

    print("Aristas ordenadas (u, v, peso):")
    for e in edges_ordenadas:
        print(f"  {e}")
    print("------------------------------------------")

    # 3. Recorrer las aristas en orden
    for (u, v, w) in edges_ordenadas:
        print(f"\nPaso {step}: Probar arista {u} -- {v} (peso {w})")

        # Si los representantes son distintos, no forma ciclo
        if uf.find(u) != uf.find(v):
            print("  -> NO forma ciclo. Se ACEPTA esta arista.")
            uf.union(u, v)
            tree_edges.append((u, v, w))
            total_cost += w
        else:
            print("  -> Forma ciclo. Se RECHAZA esta arista.")

        print("  Aristas aceptadas hasta ahora:")
        for (a, b, p) in tree_edges:
            print(f"    {a} -- {b} (peso {p})")
        print(f"  Costo acumulado: {total_cost}")
        print("------------------------------------------")

        step += 1

        # Si ya tenemos (nodos - 1) aristas, el árbol está completo
        if len(tree_edges) == len(nodos) - 1:
            break

    print("\n====== RESULTADO FINAL ======")
    print("Aristas del árbol encontrado:")
    for (u, v, w) in tree_edges:
        print(f"  {u} -- {v} (peso {w})")
    print(f"Costo total del árbol: {total_cost}")

    return tree_edges, total_cost, nodos


# ======= CONSTRUCCIÓN DEL GRAFO =======

def crear_grafo_ejemplo():
    """
    Crea una lista de aristas de ejemplo.
    Grafo NO dirigido.
    """
    edges = [
        ("A", "B", 5),
        ("A", "C", 3),
        ("B", "C", 10),
        ("B", "D", 2),
        ("C", "D", 4),
        ("C", "E", 5),
        ("D", "E", 1)
    ]
    return edges


def construir_grafo_networkx(edges):
    """
    Convierte la lista de aristas en un grafo de networkx.
    """
    G = nx.Graph()
    for (u, v, w) in edges:
        G.add_edge(u, v, weight=w)
    return G


# ======= DIBUJO CON NETWORKX =======

def dibujar_arbol(edges, tree_edges, titulo="Árbol"):
    """
    Dibuja el grafo completo y resalta el árbol (tree_edges).
    edges: lista de (u, v, w) de TODO el grafo
    tree_edges: lista de (u, v, w) del árbol encontrado
    """
    G = construir_grafo_networkx(edges)

    # Layout de nodos
    pos = nx.spring_layout(G, seed=42)

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=800)

    # Dibujar todas las aristas en gris
    nx.draw_networkx_edges(G, pos, width=2, edge_color="lightgray")

    # Etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    # Etiquetas de pesos
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    # Resaltar las aristas del árbol
    tree_edge_list = [(u, v) for (u, v, w) in tree_edges]
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=tree_edge_list,
        width=3,
        edge_color="red"
    )

    plt.title(titulo)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ======= MAIN =======

def main():
    print("==============================================")
    print(" SIMULADOR ÁRBOL DE MÍNIMO / MÁXIMO COSTE ")
    print("          ALGORITMO DE KRUSKAL")
    print("==============================================\n")

    # 1. Crear grafo de ejemplo (puedes cambiar esto)
    edges = crear_grafo_ejemplo()

    print("Aristas del grafo (u, v, peso):")
    for (u, v, w) in edges:
        print(f"  {u} -- {v} (peso {w})")
    print()

    # 2. Elegir modo: mínimo o máximo
    print("Elige modo de Kruskal:")
    print("  1) Árbol de MÍNIMO coste")
    print("  2) Árbol de MÁXIMO coste")
    opcion = input("Opción (1/2): ").strip()

    if opcion == "2":
        modo = "maximo"
    else:
        modo = "minimo"

    # 3. Ejecutar Kruskal
    tree_edges, total_cost, nodos = kruskal(edges, modo=modo)

    # 4. Dibujar el resultado
    if tree_edges:
        titulo = "Árbol de MÍNIMO coste (Kruskal)" if modo == "minimo" \
                else "Árbol de MÁXIMO coste (Kruskal)"
        dibujar_arbol(edges, tree_edges, titulo=titulo)
    else:
        print("No se pudo construir el árbol. No se dibuja la gráfica.")

    print("\nFin de la simulación.\n")


if __name__ == "__main__":
    main()
