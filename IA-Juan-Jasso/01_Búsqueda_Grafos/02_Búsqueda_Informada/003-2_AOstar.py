# Búsqueda AO* (Concepto Simplificado para la Decisión)

def calcular_decision_ao(nodo, grafo, heuristica):
    """
    Simula la decisión clave de AO*: 
    Evaluar los costos de las ramas OR y AND y elegir la que ofrezca el menor costo.
    """
    
    mejor_costo = float('inf')
    mejor_accion = None
    
    # 1. ACCESO CORRECTO a las ramas del nodo
    ramas_nodo = grafo.get(nodo, {}) 

    # 2. EVALUACIÓN DE ARCOS OR (Elige la opción con el menor costo total estimado)
    # CORRECCIÓN CLAVE: Usar ramas_nodo.get('OR', [])
    if 'OR' in ramas_nodo:
        for (sucesor, costo_accion) in ramas_nodo['OR']: 
            # Costo: Costo_Accion + h(Sucesor)
            costo_estimado = costo_accion + heuristica.get(sucesor, float('inf'))
            
            if costo_estimado < mejor_costo:
                mejor_costo = costo_estimado
                mejor_accion = f"OR: Tomar la acción hacia '{sucesor}'"

    # 3. EVALUACIÓN DE ARCOS AND (Suma de los costos de todos los subproblemas)
    # CORRECCIÓN CLAVE: Usar ramas_nodo.get('AND', [])
    if 'AND' in ramas_nodo:
        costo_and_total = 0
        sucesores_and = []
        
        for (sucesor, costo_accion) in ramas_nodo['AND']:
            # Costo: Costo_Accion + h(Sucesor)
            costo_and_total += (costo_accion + heuristica.get(sucesor, float('inf')))
            sucesores_and.append(sucesor)
            
        if costo_and_total < mejor_costo:
            mejor_costo = costo_and_total
            mejor_accion = f"AND: Resolver los subproblemas: {sucesores_and}"
        
    return mejor_costo, mejor_accion

# Definición del Grafo AND/OR:
AND_OR_GRAFO = {
    'P1': {'OR': [('P2', 1)], 'AND': [('P3', 2), ('P4', 2)]},
    'P2': {'OR': [('RESUELTO', 0)]},
    'P3': {'OR': [('RESUELTO', 0)]},
    'P4': {'OR': [('RESUELTO', 0)]},
    'RESUELTO': {} # Nodo terminal con costo 0
}

# Heurística h(n): Estimación del costo para resolver el subproblema
heuristica_ao = {
    'P1': 10,  
    'P2': 5,    
    'P3': 3,    
    'P4': 4,    
    'RESUELTO': 0
}

INICIO = 'P1'

print("Grafo AND/OR (Descomposiciones):")
for nodo, ramas in AND_OR_GRAFO.items():
    print(f"  {nodo}: {ramas}")
print(f"Heurística h(n): {heuristica_ao}")
print("-" * 50)

# Simulación de la evaluación AO* en el nodo inicial
costo, decision = calcular_decision_ao(INICIO, AND_OR_GRAFO, heuristica_ao)

print(f"Evaluando el problema inicial '{INICIO}':")
print("  Costo estimado (OR): 1 + h(P2) = 6")
print("  Costo estimado (AND): (2 + h(P3)) + (2 + h(P4)) = 11")
print("-" * 50)
print("Resultado AO* (Mejor Plan de Solución):")
print(f"  Decisión Óptima: {decision}")
print(f"  Costo Estimado: {costo}")