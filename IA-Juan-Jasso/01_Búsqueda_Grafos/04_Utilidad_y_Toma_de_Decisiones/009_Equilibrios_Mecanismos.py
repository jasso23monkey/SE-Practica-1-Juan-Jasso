import numpy as np

# Definición de la Matriz de Utilidades (Payoffs)
# La clave es (P1_utilidad, P2_utilidad)
# Indices: 0 = Confesar (C), 1 = No Confesar (NC)
PAYOFFS = {
    # P2: Confesar (0)   | P2: No Confesar (1)
    'C': { 
        'C': (-5, -5),    # Ambos confiesan: (5 años, 5 años)
        'NC': (0, -10)    # P1 libre, P2 10 años
    },
    # P1: No Confesar (1)
    'NC': {
        'C': (-10, 0),    # P1 10 años, P2 libre
        'NC': (-1, -1)     # Ambos cooperan: (1 año, 1 año)
    }
}

ACCIONES = ['C', 'NC']
P1_INDEX = 0
P2_INDEX = 1

def encontrar_mejor_respuesta(jugador_id, estrategia_oponente):
    """
    Calcula la mejor acción que un jugador puede tomar
    dado que el oponente ya ha fijado su estrategia.
    """
    mejor_utilidad = -np.inf
    mejor_accion = None
    
    # El jugador 1 está evaluando
    if jugador_id == P1_INDEX:
        for p1_accion in ACCIONES:
            utilidad = PAYOFFS[p1_accion][estrategia_oponente][P1_INDEX]
            if utilidad > mejor_utilidad:
                mejor_utilidad = utilidad
                mejor_accion = p1_accion
        return mejor_accion, mejor_utilidad
    
    # El jugador 2 está evaluando
    else:
        for p2_accion in ACCIONES:
            # La matriz se accede como PAYOFFS[P1_ACCION][P2_ACCION]
            utilidad = PAYOFFS[estrategia_oponente][p2_accion][P2_INDEX]
            if utilidad > mejor_utilidad:
                mejor_utilidad = utilidad
                mejor_accion = p2_accion
        return mejor_accion, mejor_utilidad


def buscar_equilibrio_nash():
    """
    Encuentra el Equilibrio de Nash probando todas las combinaciones.
    Un NE ocurre cuando la acción de A es la mejor respuesta a la acción de B,
    Y la acción de B es la mejor respuesta a la acción de A.
    """
    equilibrios = []
    
    for p1_estrategia in ACCIONES:
        for p2_estrategia in ACCIONES:
            
            # 1. ¿Es p1_estrategia la mejor respuesta a p2_estrategia?
            p1_mejor_resp, _ = encontrar_mejor_respuesta(P1_INDEX, p2_estrategia)
            es_p1_mejor = (p1_estrategia == p1_mejor_resp)
            
            # 2. ¿Es p2_estrategia la mejor respuesta a p1_estrategia?
            p2_mejor_resp, _ = encontrar_mejor_respuesta(P2_INDEX, p1_estrategia)
            es_p2_mejor = (p2_estrategia == p2_mejor_resp)
            
            if es_p1_mejor and es_p2_mejor:
                utilidad_p1, utilidad_p2 = PAYOFFS[p1_estrategia][p2_estrategia]
                
                equilibrios.append({
                    'P1': p1_estrategia,
                    'P2': p2_estrategia,
                    'Utilidad': (utilidad_p1, utilidad_p2)
                })

    return equilibrios

# Ejecución y Análisis
print("--- Determinando el Equilibrio de Nash (NE) ---")

# Verificar las mejores respuestas de P1
p1_br_c, _ = encontrar_mejor_respuesta(P1_INDEX, 'C')
p1_br_nc, _ = encontrar_mejor_respuesta(P1_INDEX, 'NC')
print(f"Mejor respuesta de P1 si P2 Confiesa (C): {p1_br_c}")
print(f"Mejor respuesta de P1 si P2 No Confiesa (NC): {p1_br_nc}")

print("\nBuscando el Equilibrio...")
resultado_ne = buscar_equilibrio_nash()

if resultado_ne:
    print("\nEquilibrio de Nash Encontrado:")
    for ne in resultado_ne:
        print(f"  P1: {ne['P1']}, P2: {ne['P2']} | Utilidades: {ne['Utilidad']}")
        print("  Resultado Social (Subóptimo): Ambos reciben 5 años de cárcel.")
else:
    print("\nNo se encontró un Equilibrio de Nash en estrategias puras.")