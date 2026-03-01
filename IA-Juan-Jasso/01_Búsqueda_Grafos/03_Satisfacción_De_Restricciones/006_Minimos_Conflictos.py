import random

N = 8  # Tamaño del tablero: 8x8
MAX_ITERACIONES = 1000

# --- Funciones de Utilidad ---

def contar_ataques(tablero, columna_actual, fila_actual):
    """Cuenta el número de reinas que atacan una posición específica (fila, col).
    No cuenta la reina en (columna_actual, fila_actual)."""
    
    ataques = 0
    n = len(tablero)
    
    for col in range(n):
        if col == columna_actual:
            continue  # No se chequea conflicto consigo misma

        fila_vecina = tablero[col]

        # 1. Ataque en la misma fila
        if fila_vecina == fila_actual:
            ataques += 1
        
        # 2. Ataque en la misma diagonal
        elif abs(col - columna_actual) == abs(fila_vecina - fila_actual):
            ataques += 1
            
    return ataques

def obtener_total_conflictos(tablero):
    """Calcula el número total de pares de reinas que se atacan en el tablero."""
    total_conflictos = 0
    n = len(tablero)
    
    for col in range(n):
        # Para evitar contar pares de ataques dos veces, solo chequeamos conflictos 
        # en el contexto de la posición actual, y no con sus vecinos futuros.
        # Es más fácil y preciso que la suma directa.
        total_conflictos += contar_ataques(tablero, col, tablero[col])
        
    # Como contar_ataques cuenta (A ataca B) y (B ataca A), dividimos entre 2.
    return total_conflictos // 2 

# --- Algoritmo Mínimos-Conflictos ---

def min_conflicts_search(N):
    # 1. Inicialización: Colocación aleatoria, una reina por columna.
    # El tablero es una lista, donde el índice es la columna y el valor es la fila.
    tablero = [random.randint(0, N - 1) for _ in range(N)]
    
    for iteracion in range(MAX_ITERACIONES):
        conflictos_actuales = obtener_total_conflictos(tablero)
        
        # Condición de Éxito: Cero conflictos
        if conflictos_actuales == 0:
            return tablero, iteracion
        
        # 2. Selección de Variable: Elegir una columna (reina) que esté en conflicto
        columnas_en_conflicto = []
        for col in range(N):
            if contar_ataques(tablero, col, tablero[col]) > 0:
                columnas_en_conflicto.append(col)
        
        # Elegir una columna al azar entre las conflictivas
        columna_a_mover = random.choice(columnas_en_conflicto)
        
        # 3. Selección del Valor (Mínimos-Conflictos)
        mejor_fila = tablero[columna_a_mover]
        min_conflictos = contar_ataques(tablero, columna_a_mover, mejor_fila)
        
        mejores_filas_posibles = []

        # Evaluar todas las posibles filas para la columna seleccionada
        for fila in range(N):
            conflictos_si_muevo = contar_ataques(tablero, columna_a_mover, fila)
            
            if conflictos_si_muevo < min_conflictos:
                min_conflictos = conflictos_si_muevo
                mejores_filas_posibles = [fila] # Reiniciar la lista
            elif conflictos_si_muevo == min_conflictos:
                mejores_filas_posibles.append(fila) # Mantener empate
        
        # 4. Movimiento: Elegir una fila al azar entre las que minimizan conflictos
        if mejores_filas_posibles:
            nueva_fila = random.choice(mejores_filas_posibles)
            tablero[columna_a_mover] = nueva_fila

        # Salida para seguimiento
        if iteracion % 50 == 0 or iteracion < 5:
            print(f"Iter {iteracion:03d}: Conflictos = {conflictos_actuales}, Moviendo Q{columna_a_mover} a fila {nueva_fila}")

    return tablero, MAX_ITERACIONES # Falla si se alcanza el límite

# Ejecución
solucion, iteraciones = min_conflicts_search(N)

print("\n" + "="*50)
if obtener_total_conflictos(solucion) == 0:
    print(f"ÉXITO: ¡Solución encontrada en {iteraciones} iteraciones!")
    print(f"Tablero (Columna -> Fila): {solucion}")
else:
    print(f"FALLO: El algoritmo se atascó después de {MAX_ITERACIONES} iteraciones.")
    print(f"Mejor estado encontrado (Conflictos: {obtener_total_conflictos(solucion)}): {solucion}")