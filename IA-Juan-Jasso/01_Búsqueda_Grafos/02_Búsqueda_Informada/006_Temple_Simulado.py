# Búsqueda de Temple Simulado (Simulated Annealing)

import random
import math

# Función de Costo: Número de ataques (Queremos MINIMIZAR este valor a 0)
def calcular_costo(tablero):
    """
    Calcula el número de pares de reinas que se atacan.
    El mínimo es 0 (solución perfecta).
    """
    ataques = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            # Ataque en la misma fila (no sucede en esta representación) o diagonal
            if abs(i - j) == abs(tablero[i] - tablero[j]):
                ataques += 1
    return ataques

# Función para generar un vecino aleatorio
def generar_vecino(tablero):
    """
    Genera un nuevo estado moviendo una reina aleatoria a una nueva fila aleatoria.
    """
    n = len(tablero)
    nuevo_tablero = list(tablero)
    
    # Elige una columna (reina) para mover
    columna_a_mover = random.randint(0, n - 1)
    
    # Elige una nueva fila
    nueva_fila = random.randint(0, n - 1)
    
    # Asegura que el movimiento no sea al mismo lugar, aunque no es estrictamente necesario
    while nueva_fila == tablero[columna_a_mover]:
        nueva_fila = random.randint(0, n - 1)

    nuevo_tablero[columna_a_mover] = nueva_fila
    return tuple(nuevo_tablero)

def temple_simulado(n=8, T_inicial=1.0, T_final=0.0001, factor_enfriamiento=0.99):
    # 1. ESTADO INICIAL ALEATORIO
    tablero_actual = tuple(random.randint(0, n - 1) for _ in range(n))
    costo_actual = calcular_costo(tablero_actual)
    
    mejor_tablero_global = tablero_actual
    mejor_costo_global = costo_actual
    
    T = T_inicial # Temperatura inicial
    iteracion = 0
    
    print(f"Inicio: Costo={costo_actual}, T={T_inicial}")

    while T > T_final:
        iteracion += 1
        
        # 2. GENERAR VECINO
        tablero_vecino = generar_vecino(tablero_actual)
        costo_vecino = calcular_costo(tablero_vecino)
        
        # 3. CÁLCULO DE LA DIFERENCIA DE ENERGÍA
        Delta_E = costo_vecino - costo_actual 
        
        # 4. CRITERIO DE ACEPTACIÓN
        if Delta_E < 0:
            # Opción A: El vecino es mejor (costo menor) -> Siempre aceptar
            aceptar = True
        else:
            # Opción B: El vecino es peor (costo mayor) -> Aceptar con probabilidad P
            # P = e^(-Delta_E / T)
            probabilidad = math.exp(-Delta_E / T)
            aceptar = random.random() < probabilidad
        
        # 5. TRANSICIÓN DE ESTADO
        if aceptar:
            tablero_actual = tablero_vecino
            costo_actual = costo_vecino
            
            # Actualizar el mejor estado global
            if costo_actual < mejor_costo_global:
                mejor_costo_global = costo_actual
                mejor_tablero_global = tablero_actual
                # print(f"  Nuevo Mejor Global: Costo={mejor_costo_global}")
                
            if mejor_costo_global == 0:
                break # Solución óptima encontrada

        # 6. ENFRIAMIENTO (Recocido Geométrico)
        T *= factor_enfriamiento 
        
        # Evitar demasiada salida para el bucle
        if iteracion % 500 == 0:
            print(f"Iter: {iteracion}, Costo Actual: {costo_actual}, T: {T:.4f}, Mejor Global: {mejor_costo_global}")


    return mejor_tablero_global, mejor_costo_global

# Ejecución del algoritmo
SOLUCION_OPT = 0 # El valor de costo ideal (cero ataques)
print("Configuración: T_inicial=1.0, Factor_enfriamiento=0.99")
resultado_tablero, resultado_costo = temple_simulado()

print("-" * 70)
print("Resultado Final (Mejor Global Encontrado):")
print(f"  Tablero: {resultado_tablero}")
print(f"  Costo (Ataques): {resultado_costo} / {SOLUCION_OPT} (Mínimo)")

if resultado_costo == SOLUCION_OPT:
    print("  ¡Éxito! Temple Simulado encontró la solución óptima (cero ataques).")
else:
    print("  La búsqueda finalizó sin alcanzar el óptimo global.")