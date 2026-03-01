import networkx as nx
import matplotlib.pyplot as plt

# ======= ESTRUCTURAS AUXILIARES (UNION-FIND) =======
class UnionFind:
    """
    Estructura para gestionar conjuntos disjuntos. 
    Evita que la IA cree 'bucles' sociales redundantes.
    """
    def __init__(self, elementos):
        self.parent = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

# ======= LÓGICA DE KRUSKAL (SOCIALIZACIÓN) =======
def kruskal_boda(edges, modo="minimo"):
    nodos = set()
    for (u, v, w) in edges:
        nodos.add(u)
        nodos.add(v)

    # Ordenar según el nivel de timidez (Data)
    if modo == "minimo":
        edges_ordenadas = sorted(edges, key=lambda x: x[2])
        print("\n=== PLANIFICADOR KRUSKAL: MÍNIMA TIMIDEZ ===")
    else:
        edges_ordenadas = sorted(edges, key=lambda x: x[2], reverse=True)
        print("\n=== PLANIFICADOR KRUSKAL: MÁXIMA INTEGRACIÓN ===")

    uf = UnionFind(nodos)
    tree_edges = []
    total_shyness = 0
    step = 1

    print(f"Analizando data de {len(nodos)} grupos sociales...")
    print("-" * 50)

    for (u, v, w) in edges_ordenadas:
        # Arrojando resultados basados en la data
        if uf.find(u) != uf.find(v):
            print(f"Paso {step}: Presentar a [{u}] con [{v}] (Dificultad: {w})")
            print("  -> Resultado: ACEPTADO. Nueva conexión social establecida.")
            uf.union(u, v)
            tree_edges.append((u, v, w))
            total_shyness += w
            step += 1
        else:
            print(f"Paso {step}: Omitir presentación [{u}]--[{v}]")
            print("  -> Resultado: RECHAZADO. Ya tienen un conocido en común.")
        
        if len(tree_edges) == len(nodos) - 1:
            break

    print("\n====== CONCLUSIÓN DE LA IA ======")
    print(f"Para integrar la fiesta por completo, realiza estas {len(tree_edges)} presentaciones.")
    print(f"Nivel de timidez total superado: {total_shyness}")
    return tree_edges, total_shyness, nodos

# ======= DATA DE LA FIESTA =======
def crear_datos_boda():
    # Formato: (Grupo_A, Grupo_B, Nivel_de_Timidez_1_al_10)
    # Entre más bajo el número, más rápido se llevan bien.
    data = [
        ("Familia_Novia", "Familia_Novio", 9),
        ("Familia_Novia", "Primos_Jóvenes", 2),
        ("Amigos_Prepa", "Compañeros_Trabajo", 5),
        ("Amigos_Prepa", "Familia_Novio", 10),
        ("Primos_Jóvenes", "Amigos_Prepa", 3),
        ("Compañeros_Trabajo", "Familia_Novia", 7),
        ("Primos_Jóvenes", "Compañeros_Trabajo", 4)
    ]
    return data

# ======= VISUALIZACIÓN DEL GRAFO =======
def dibujar_mapa_social(edges, tree_edges, titulo):
    G = nx.Graph()
    for (u, v, w) in edges:
        G.add_edge(u, v, weight=w)

    # Layout circular para simular mesas de una fiesta
    pos = nx.circular_layout(G)
    plt.figure(figsize=(10, 7))

    # Dibujar grupos sociales
    nx.draw_networkx_nodes(G, pos, node_size=3500, node_color="#ff9eb5", edgecolors="black")
    
    # Dibujar todas las posibles charlas en gris
    nx.draw_networkx_edges(G, pos, width=1, edge_color="lightgray", style="--", alpha=0.6)
    
    # Resaltar en VERDE las presentaciones clave arrojadas por Kruskal
    tree_edge_list = [(u, v) for (u, v, w) in tree_edges]
    nx.draw_networkx_edges(G, pos, edgelist=tree_edge_list, width=5, edge_color="#2ecc71")

    # Etiquetas
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title(titulo, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# ======= FUNCIÓN PRINCIPAL =======
def main():
    print("==============================================")
    print("     ORGANIZADOR SOCIAL DE EVENTOS (IA)       ")
    print("==============================================\n")

    edges = crear_datos_boda()
    
    print("Selecciona el objetivo de la fiesta:")
    print("1. Integración fluida (Mínima timidez)")
    print("2. Romper el hielo extremo (Máxima integración)")
    op = input("Selección (1/2): ").strip()

    modo = "maximo" if op == "2" else "minimo"
    
    # Ejecución del algoritmo
    arbol_social, timidez_total, nodos_fiesta = kruskal_boda(edges, modo=modo)

    # Mostrar la gráfica resultante
    if arbol_social:
        tit_grafica = f"Mapa de Socialización: Modo {modo.capitalize()}"
        dibujar_mapa_social(edges, arbol_social, tit_grafica)

if __name__ == "__main__":
    main()