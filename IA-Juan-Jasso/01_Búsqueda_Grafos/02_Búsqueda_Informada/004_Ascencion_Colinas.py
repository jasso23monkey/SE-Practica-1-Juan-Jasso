# Búsqueda de Ascensión de Colinas (Steepest Ascent)

import random

# Función de Valoración (Heurística): Número de pares de reinas que NO se atacan
def evaluar_estado(tablero):
    """
    Calcula la "bondad" del tablero. Queremos MAXIMIZAR este valor.
    El máximo posible de pares que no se atacan es 8 * 7 / 2 = 28.
    """
    ataques = 0
    n = len(tablero) # 8
    
    # Comprobar ataques por pares
    for i in range(n):
        for j in range(i + 1, n):
            # Ataque en la misma fila (no debería ocurrir en esta representación)
            if tablero[i] == tablero[j]:
                ataques += 1
            # Ataque en diagonal: |fila1 - fila2| == |columna1 - columna2|
            elif abs(i - j) == abs(tablero[i] - tablero[j]):
                ataques += 1
                
    # La bondad (valoración) es el total de pares menos los ataques
    total_pares = n * (n - 1) // 2 
    valoracion = total_pares - ataques
    return valoracion

# Función para obtener todos los vecinos (moviendo una reina por una columna)
def obtener_vecinos(tablero):
    n = len(tablero)
    vecinos = []
    
    # Iterar sobre cada columna (i)
    for i in range(n):
        # Iterar sobre cada fila (nueva_pos) para esa columna
        for nueva_pos in range(n):
            if tablero[i] != nueva_pos: # Solo si el movimiento es real
                nuevo_tablero = list(tablero)
                nuevo_tablero[i] = nueva_pos # Mueve la reina de columna i a la nueva_pos
                vecinos.append(tuple(nuevo_tablero))
                
    return vecinos

def hill_climbing(n=8):
    # 1. ESTADO INICIAL ALEATORIO
    # El tablero es una tupla donde el índice es la columna y el valor es la fila
    tablero_actual = tuple(random.randint(0, n - 1) for _ in range(n))
    valoracion_actual = evaluar_estado(tablero_actual)
    
    print(f"Inicio: {tablero_actual} (Valoración: {valoracion_actual})")
    
    while True:
        mejor_vecino = None
        mejor_valoracion = valoracion_actual
        
        # 2. EVALUACIÓN DE VECINOS (Steepest Ascent)
        for vecino in obtener_vecinos(tablero_actual):
            valoracion_vecino = evaluar_estado(vecino)
            
            # Buscar el vecino que MAXIMIZA la función de valoración
            if valoracion_vecino > mejor_valoracion:
                mejor_valoracion = valoracion_vecino
                mejor_vecino = vecino
        
        # 3. CRITERIO DE PARADA
        if mejor_valoracion <= valoracion_actual:
            # No se encontró un vecino mejor (Se alcanzó un óptimo local o global)
            return tablero_actual, valoracion_actual
        
        # 4. TRANSICIÓN DE ESTADO (Ascenso)
        tablero_actual = mejor_vecino
        valoracion_actual = mejor_valoracion
        print(f"Ascenso: {tablero_actual} (Valoración: {valoracion_actual})")

# Ejecución del algoritmo
SOLUCION_OPT = 28 # El valor de valoración ideal (máximo de pares sin atacar)
resultado_tablero, resultado_valoracion = hill_climbing()

print("-" * 50)
print("Resultado Final:")
print(f"  Tablero: {resultado_tablero}")
print(f"  Valoración: {resultado_valoracion} / {SOLUCION_OPT} (Máximo)")

if resultado_valoracion == SOLUCION_OPT:
    print("  ¡Éxito! Se encontró una solución global (no hay ataques).")
else:
    print("  La búsqueda se detuvo en un ÓPTIMO LOCAL.")