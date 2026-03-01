# Búsqueda Tabú (Tabu Search) para las 8 Reinas

import random

# Valoración: Pares de reinas que NO se atacan (MÁXIMO 28)
def evaluar_estado(tablero):
    ataques = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            # Comprueba ataques en diagonal
            if abs(i - j) == abs(tablero[i] - tablero[j]):
                ataques += 1
    total_pares = n * (n - 1) // 2 
    return total_pares - ataques

# Función para obtener vecinos y los movimientos
def obtener_vecinos_y_movimientos(tablero):
    n = len(tablero)
    vecinos = []
    # Movimiento: (columna_movida, fila_destino)
    movimientos = [] 

    for col_origen in range(n):
        for fila_destino in range(n):
            if tablero[col_origen] != fila_destino:
                nuevo_tablero = list(tablero)
                nuevo_tablero[col_origen] = fila_destino
                
                vecinos.append(tuple(nuevo_tablero))
                # Registra el movimiento
                movimientos.append((col_origen, fila_destino))
                
    return vecinos, movimientos

def busqueda_tabu(n=8, tenencia_tabu=7, max_iteraciones=1000):
    # 1. INICIALIZACIÓN
    tablero_actual = tuple(random.randint(0, n - 1) for _ in range(n))
    valoracion_actual = evaluar_estado(tablero_actual)
    
    mejor_tablero_global = tablero_actual
    mejor_valoracion_global = valoracion_actual
    
    # Lista Tabú: Almacena los movimientos prohibidos (columna, fila_destino)
    lista_tabu = [] 
    
    print(f"Inicio: {tablero_actual} (Valoración: {valoracion_actual})")

    for iteracion in range(max_iteraciones):
        
        vecinos, movimientos = obtener_vecinos_y_movimientos(tablero_actual)
        
        mejor_movimiento_candidato = None
        mejor_valoracion_candidata = -1 # Valoración mínima posible
        tablero_siguiente = None # Aseguramos que está inicializado

        # 2. EVALUACIÓN DE VECINOS Y APLICACIÓN DE RESTRICCIONES
        for vecino, movimiento in zip(vecinos, movimientos):
            valoracion_vecino = evaluar_estado(vecino)
            
            es_tabu = movimiento in lista_tabu
            
            # Criterio de Aspiración: Se permite un movimiento tabú si lleva a un mejor global
            criterio_aspiracion = (valoracion_vecino > mejor_valoracion_global)
            
            if (not es_tabu or criterio_aspiracion) and (valoracion_vecino > mejor_valoracion_candidata):
                # Se encontró un mejor candidato (que no es tabú o cumple la aspiración)
                mejor_valoracion_candidata = valoracion_vecino
                mejor_movimiento_candidato = movimiento
                # AHORA ASIGNAMOS EL TABLERO DEL MEJOR VECINO
                tablero_siguiente = vecino 
        
        # 3. CRITERIO DE PARADA / TRANSICIÓN
        if mejor_movimiento_candidato is None or tablero_siguiente is None:
            # No hay movimientos válidos para avanzar
            break

        # Actualiza el estado actual (siempre con el mejor tablero encontrado)
        tablero_actual = tablero_siguiente
        valoracion_actual = mejor_valoracion_candidata
        
        # 4. ACTUALIZACIÓN DE MEMORIA (Lista Tabú)
        # Añade el movimiento realizado a la lista tabú
        lista_tabu.append(mejor_movimiento_candidato)
        # Mantiene la longitud de la lista tabú
        if len(lista_tabu) > tenencia_tabu:
            lista_tabu.pop(0) # Elimina el movimiento más antiguo

        # 5. ACTUALIZACIÓN DEL MEJOR GLOBAL
        if valoracion_actual > mejor_valoracion_global:
            mejor_valoracion_global = valoracion_actual
            mejor_tablero_global = tablero_actual
            # print(f"Nuevo Mejor Global: {mejor_valoracion_global}")
            
        if mejor_valoracion_global == SOLUCION_OPT:
            break
            
    return mejor_tablero_global, mejor_valoracion_global

# Ejecución del algoritmo
SOLUCION_OPT = 28 # El valor de valoración ideal (máximo de pares sin atacar)
print("Configuración: Tenencia Tabú = 7, Máx. Iteraciones = 1000")
resultado_tablero, resultado_valoracion = busqueda_tabu()

print("-" * 50)
print("Resultado Final (Mejor Global Encontrado):")
print(f"  Tablero: {resultado_tablero}")
print(f"  Valoración: {resultado_valoracion} / {SOLUCION_OPT}")

if resultado_valoracion == SOLUCION_OPT:
    print("  ¡Éxito! La Búsqueda Tabú encontró la solución óptima.")
else:
    print("  La búsqueda finalizó sin encontrar la solución óptima (posiblemente atrapada o límite de iteración).")