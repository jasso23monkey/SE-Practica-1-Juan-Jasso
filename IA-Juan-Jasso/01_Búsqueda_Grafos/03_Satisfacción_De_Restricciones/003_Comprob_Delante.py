# Comprobación Hacia Delante (Forward Checking - FC)

# --- 1. DEFINICIÓN DEL CSP Y FUNCIONES DE ASIGNACIÓN ---

VARIABLES = ['T1', 'T2', 'T3']
DOMINIOS_INICIALES = {
    'T1': ['L', 'M', 'X'],
    'T2': ['L', 'M', 'X'],
    'T3': ['L', 'M', 'X']
}
RESTRICCIONES_VECINOS = [('T1', 'T2'), ('T1', 'T3'), ('T2', 'T3')]

# --- FUNCIÓN NECESARIA PARA LA COMPROBACIÓN BÁSICA ---
def es_consistente(variable, valor, asignacion):
    """
    Verifica si asignar 'valor' a 'variable' viola alguna restricción 
    con las asignaciones que ya están hechas.
    """
    RESTRICCIONES_VECINOS = [('T1', 'T2'), ('T1', 'T3'), ('T2', 'T3')] # Definición local para el ejemplo

    for v1, v2 in RESTRICCIONES_VECINOS:
        # Chequea la restricción (v1 != v2)
        
        # 1. Caso: La variable actual es v1 y v2 ya está asignada
        if v1 == variable and v2 in asignacion:
            if valor == asignacion[v2]:
                return False

        # 2. Caso: La variable actual es v2 y v1 ya está asignada
        elif v2 == variable and v1 in asignacion:
            if valor == asignacion[v1]:
                return False
                
    return True

def forward_checking(variable, valor, asignacion, dominios_actuales):
    """
    Implementa la Comprobación Hacia Delante.
    Retorna True si no hay fallos, False si detecta un dominio vacío.
    """
    # Guardar los dominios originales antes de podar (para la vuelta atrás)
    dominios_backup = {v: list(d) for v, d in dominios_actuales.items()}
    
    # Propagación: Recorrer vecinos no asignados
    for v1, v2 in RESTRICCIONES_VECINOS:
        vecino = None
        
        # Identificar el vecino no asignado
        if v1 == variable and v2 not in asignacion:
            vecino = v2
        elif v2 == variable and v1 not in asignacion:
            vecino = v1
            
        if vecino:
            # Poda de Dominios: Si el valor es el mismo, se elimina del dominio del vecino
            if valor in dominios_actuales[vecino]:
                dominios_actuales[vecino].remove(valor)
                
                # Detección de Fallo Temprano: Si el dominio queda vacío
                if not dominios_actuales[vecino]:
                    # Restaurar dominios y fallar
                    for v, d in dominios_backup.items():
                        dominios_actuales[v] = d
                    return False
                    
    return True # Éxito en la comprobación hacia delante

# --- 2. ALGORITMO DE BACKTRACKING CON FC ---

def backtracking_con_fc(asignacion, dominios_actuales):
    
    if len(asignacion) == len(VARIABLES):
        return asignacion

    # 1. Selección de la primera variable no asignada
    variable = [v for v in VARIABLES if v not in asignacion][0]

    # 2. Intentar valores (tomados del dominio original para simplicidad)
    for valor in DOMINIOS_INICIALES[variable]:
        
        # Chequeo de Consistencia con asignaciones ya hechas (siempre necesario)
        if es_consistente(variable, valor, asignacion):
            
            # Guardar una copia profunda de los dominios para la vuelta atrás
            dominios_backup = {v: list(d) for v, d in dominios_actuales.items()}
            
            # 3. COMPROBACIÓN HACIA DELANTE
            if forward_checking(variable, valor, asignacion, dominios_actuales):
                
                # Asignación exitosa
                asignacion[variable] = valor
                
                # Llamada recursiva
                resultado = backtracking_con_fc(asignacion, dominios_actuales)
                
                if resultado is not None:
                    return resultado

                # Vuelta Atrás de Asignación y Dominios
                del asignacion[variable]
            
            # Si FC falló o la recursión falló, siempre restaurar los dominios
            dominios_actuales.clear()
            dominios_actuales.update(dominios_backup)
            
    return None

# --- 3. EJECUCIÓN Y SIMULACIÓN DE UN PASO CLAVE ---

# El algoritmo necesita una copia modificable de los dominios
dominios_modificables = {v: list(d) for v, d in DOMINIOS_INICIALES.items()}

print("Simulación de un paso de Búsqueda con Comprobación Hacia Delante:")
print(f"Dominios Iniciales: {dominios_modificables}")

# 1. Asignar T1 = Lunes (L)
print("\n--- Paso 1: Asignar T1 = L ---")

if es_consistente('T1', 'L', {}):
    
    # Aplicar FC
    if forward_checking('T1', 'L', {'T1': 'L'}, dominios_modificables):
        print("  FC OK. Dominios podados:")
        print("  T1 (Asignada a L). D(T2) y D(T3) pierden 'L'.")
        
        # En el código real, T1 se asignaría ahora. Simplemente mostramos el efecto:
        print(f"  Dominios Actuales: {dominios_modificables}") 
        
        # Ahora el algoritmo procedería a asignar T2...

# 2. Simulación de un Fallo FC (Si se intentara asignar T2 = M)
# Asumimos que T1 = L fue exitoso, y ahora T2 solo tiene ['M', 'X'] y T3 solo tiene ['M', 'X'].
# Intentamos asignar T2 = M.

dominios_modificables_fallo = {'T1': [], 'T2': ['M', 'X'], 'T3': ['M', 'X']}
print("\n--- Paso 2: Asignar T2 = M ---")

if es_consistente('T2', 'M', {'T1': 'L'}):
    # Aplicar FC
    if forward_checking('T2', 'M', {'T1': 'L', 'T2': 'M'}, dominios_modificables_fallo):
        # ... (Esto nunca sucederá porque T3 se queda sin opciones)
        pass 
    else:
        print("  !!! FC Falló y detectó Vuelta Atrás Necesaria. !!!")
        print("  Razón: Asignar T2='M' obligó a podar 'M' del dominio de T3, dejando D(T3) vacío.")
        
# Finalmente, ejecutar la búsqueda completa
solucion = backtracking_con_fc({}, {v: list(d) for v, d in DOMINIOS_INICIALES.items()})

print("\n--- Resultado de la Búsqueda Completa ---")
if solucion:
    print(f"Solución final: {solucion}")