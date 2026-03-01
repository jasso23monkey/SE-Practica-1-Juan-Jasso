# Simulación de Salto Atrás Dirigido por Conflictos (CBJ)

# Definición del problema
VARIABLES = ['V1', 'V2', 'V3', 'V4']
RESTRICCIONES_CLAVE = {
    'V4': ['V1', 'V3'] # V4 está restringida por V1 y V3
}

# --- FUNCIÓN SIMULADA PARA IDENTIFICAR CONFLICTO ---

def obtener_conjunto_conflicto(variable_fallida, asignacion_actual, valor_intentado):
    """
    Simula la identificación de variables asignadas que causan un fallo
    al intentar asignar 'variable_fallida' = 'valor_intentado'.
    """
    conflicto = set()
    
    # 1. Itera sobre las variables que restringen a la variable_fallida
    for vecino in RESTRICCIONES_CLAVE.get(variable_fallida, []):
        if vecino in asignacion_actual:
            
            # 2. Simulación de la regla de restricción: Si los valores son iguales, hay conflicto
            # En un CSP real, la restricción sería V1 != V4.
            if asignacion_actual[vecino] == valor_intentado:
                conflicto.add(vecino)
                
    return conflicto

# --- SIMULACIÓN DEL ALGORITMO CON CBJ ---

def simular_cbj():
    asignacion = {}
    
    # --- PASO 1: Asignaciones Iniciales ---
    print("--- 1. Asignaciones Iniciales ---")
    
    # Asignación Culpable (Early Assignment)
    asignacion['V1'] = 1 
    print("Asignación: V1 = 1 (La Causa Raíz)")
    
    # Asignación Inocente (Traditional Backtracking fallaría aquí)
    asignacion['V2'] = 2 
    print("Asignación: V2 = 2 (Inocente)")
    
    # Asignación Inocente (Traditional Backtracking fallaría aquí)
    asignacion['V3'] = 3
    print("Asignación: V3 = 3 (Inocente)")
    
    # --- PASO 2: La Búsqueda Falla en V4 ---
    
    variable_fallida = 'V4'
    dominios_V4 = [1, 2, 3]
    
    print("\n--- 2. Búsqueda y Conflicto en V4 ---")
    conflicto_general = set()
    
    for valor in dominios_V4:
        print(f"  Intentando V4 = {valor}...")
        
        # Obtener las variables que causan el fallo para este valor
        conflicto_actual = obtener_conjunto_conflicto(variable_fallida, asignacion, valor)
        
        if not conflicto_actual:
            # Si el conflicto actual está vacío, el valor es consistente.
            # En nuestro ejemplo simulado, esto ocurre solo si valor=2.
            if valor != 2: # Forzar el conflicto para valores 1 y 3
                conflicto_actual = {'V1'} if valor == 1 else {'V3'}

        if conflicto_actual:
            print(f"    -> FALLO. En conflicto con: {conflicto_actual}")
            conflicto_general.update(conflicto_actual)
        else:
            # Si valor = 2, no hay conflicto. En un CSP real, se movería a la siguiente variable.
            # Aquí asumimos que todos los valores terminan fallando después de más asignaciones.
            pass 
            
    # Asumimos que la rama falla por completo (todos los valores para V4 no funcionan)
    print("\n  ** Dominio de V4 agotado. Se requiere Salto Atrás. **")
    
    # --- PASO 3: Salto Atrás Dirigido por Conflictos ---
    
    print(f"  Conflicto General de V4: {conflicto_general}") 
    
    # Identificar la variable asignada más reciente en el conjunto de conflicto
    variables_asignadas_ordenadas = [v for v in VARIABLES if v in asignacion] # ['V1', 'V2', 'V3']
    
    indice_salto = -1
    destino_salto = None
    
    # Encontrar la variable asignada más reciente entre las conflictivas
    for i in range(len(variables_asignadas_ordenadas) - 1, -1, -1):
        v = variables_asignadas_ordenadas[i]
        if v in conflicto_general:
            destino_salto = v
            indice_salto = i
            break

    # Simular la acción de CBJ
    print("\n--- 3. Acción CBJ ---")
    if destino_salto:
        print("La Búsqueda Tradicional retrocedería a: V3")
        
        # El CBJ salta directamente a la variable culpable más reciente
        variables_saltadas = variables_asignadas_ordenadas[indice_salto + 1:]
        
        print(f"CBJ salta DIRECTAMENTE a: {destino_salto}")
        print(f"Variables saltadas (no culpables): {variables_saltadas}")
    else:
        print("No se encontraron variables de conflicto asignadas.")

simular_cbj()