# Búsqueda de Haz Local (Local Beam Search)

import random

# Función de Valoración (Queremos MAXIMIZAR a 28)
def evaluar_estado(tablero):
    ataques = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(tablero[i] - tablero[j]):
                ataques += 1
    total_pares = n * (n - 1) // 2 
    return total_pares - ataques

# Función para obtener TODOS los vecinos de un estado
def obtener_todos_vecinos(tablero):
    n = len(tablero)
    vecinos = set() # Usamos un conjunto para evitar duplicados
    
    for col_origen in range(n):
        for fila_destino in range(n):
            if tablero[col_origen] != fila_destino:
                nuevo_tablero = list(tablero)
                nuevo_tablero[col_origen] = fila_destino
                vecinos.add(tuple(nuevo_tablero))
                
    return vecinos

def busqueda_haz_local(n=8, k=5, max_iteraciones=100):
    """
    Implementa Búsqueda de Haz Local con un tamaño de haz k.
    """
    
    # 1. INICIALIZACIÓN: Crear un Haz inicial de k estados aleatorios
    haz_actual = set()
    for _ in range(k):
        tablero = tuple(random.randint(0, n - 1) for _ in range(n))
        haz_actual.add(tablero)
        
    mejor_valoracion_global = -1
    mejor_tablero_global = None
    
    print(f"LBS (k={k}) iniciado. Iteración → Mejor Global")

    for iteracion in range(max_iteraciones):
        todos_sucesores = []
        
        # 2. GENERAR TODOS LOS SUCESORES DEL HAZ
        for tablero in haz_actual:
            valoracion = evaluar_estado(tablero)
            if valoracion > mejor_valoracion_global:
                mejor_valoracion_global = valoracion
                mejor_tablero_global = tablero
                
            # Si se encuentra la solución óptima, detener
            if mejor_valoracion_global == (n * (n - 1) // 2):
                return mejor_tablero_global, mejor_valoracion_global

            # Generar y evaluar los sucesores
            for vecino in obtener_todos_vecinos(tablero):
                valoracion_vecino = evaluar_estado(vecino)
                # Almacenar (valoracion, tablero) para ordenarlos después
                todos_sucesores.append((valoracion_vecino, vecino))
        
        # 3. SELECCIÓN DEL NUEVO HAZ (Determinista: los k mejores)
        # Ordenar por valoración de forma descendente y tomar los k primeros
        todos_sucesores.sort(key=lambda x: x[0], reverse=True)
        
        # El nuevo haz es el conjunto de los tableros de los k mejores sucesores
        nuevo_haz = set()
        for _, tablero in todos_sucesores[:k]:
            nuevo_haz.add(tablero)
        
        # 4. TRANSICIÓN
        if not nuevo_haz:
            # Caso de parada si no hay sucesores válidos
            break 
            
        haz_actual = nuevo_haz
        
        print(f"Iteración {iteracion + 1}: {mejor_valoracion_global} (Haz de {len(haz_actual)} estados)")
        
    return mejor_tablero_global, mejor_valoracion_global

# Ejecución del algoritmo
N = 8
SOLUCION_OPT = N * (N - 1) // 2 # 28
print(f"Problema: {N} Reinas. Objetivo de Valoración: {SOLUCION_OPT}")
resultado_tablero, resultado_valoracion = busqueda_haz_local(n=N, k=10, max_iteraciones=20)

print("-" * 50)
print("Resultado Final (LBS):")
print(f"  Tablero: {resultado_tablero}")
print(f"  Valoración: {resultado_valoracion} / {SOLUCION_OPT}")

if resultado_valoracion == SOLUCION_OPT:
    print("  ¡Éxito! Se encontró la solución óptima.")
else:
    print("  La búsqueda finalizó sin alcanzar el óptimo global.")