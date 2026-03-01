from collections import deque

# --- 1. DEFINICIÓN DEL CSP ---
VARIABLES = ['A', 'B', 'C']

DOMINIOS = {
    'A': ['Rojo', 'Verde', 'Azul'],
    'B': ['Rojo', 'Verde', 'Azul'],
    'C': ['Rojo', 'Verde', 'Azul']
}

# Vecinos conectados por restricciones binarias
RESTRICCIONES_BINARIAS = {
    'A': ['B'], 
    'B': ['A', 'C'],
    'C': ['B']
}

# --- 2. FUNCIÓN DE REVISIÓN DE ARCO ---

def revisar_arco(Vi, Vj, dominios_actuales):
    """
    Revisa la consistencia del arco (Vi, Vj) y poda el dominio de Vi si es necesario.
    Retorna True si el dominio de Vi fue modificado.
    """
    modificado = False
    
    # 1. Chequeo de Consistencia: Si Vi != Vj
    valores_a_eliminar = []
    
    for x in dominios_actuales[Vi]:
        # Suponemos que x no tiene soporte en Dj
        tiene_soporte = False
        
        # Buscar al menos un valor 'y' en Dj que satisfaga la restricción
        for y in dominios_actuales[Vj]:
            # La restricción es simple: x debe ser diferente de y (x != y)
            if x != y: 
                tiene_soporte = True
                break
        
        # Si NO encontramos soporte para 'x' en Dj, lo marcamos para eliminar
        if not tiene_soporte:
            valores_a_eliminar.append(x)
            
    # 2. Poda: Eliminar los valores inconsistentes de Di
    if valores_a_eliminar:
        modificado = True
        for valor in valores_a_eliminar:
            dominios_actuales[Vi].remove(valor)
            
    return modificado

# --- 3. ALGORITMO AC-3 ---

def AC3(dominios):
    """
    Aplica el algoritmo AC-3 a los dominios para alcanzar la Consistencia de Arco.
    """
    # 0. Inicializar la cola con todos los arcos binarios (doblemente)
    cola = deque()
    for v1 in VARIABLES:
        for v2 in RESTRICCIONES_BINARIAS.get(v1, []):
            cola.append((v1, v2))

    print(f"Inicio AC-3. Cola inicial con {len(cola)} arcos.")
    
    while cola:
        Vi, Vj = cola.popleft()
        
        # 1. Revisar el arco
        if revisar_arco(Vi, Vj, dominios):
            print(f"  Dominio de {Vi} reducido: {dominios[Vi]}.")
            
            # 2. Propagar cambios: Si Vi fue modificado, añadir todos los arcos (Vk, Vi) a la cola
            if not dominios[Vi]:
                return False  # Fallo: Dominio vacío, el CSP no tiene solución
            
            for Vk in RESTRICCIONES_BINARIAS.get(Vi, []):
                # Añadir arcos donde Vk es vecino de Vi (Vk != Vj)
                if Vk != Vj: 
                    cola.append((Vk, Vi))
                    
    return True # El CSP es consistente en arco

# ===================================================
# --- EJECUCIÓN DEL CSP CON PROPAGACIÓN ---
# ===================================================

# 1. Aplicar Consistencia de Nodo (Restricción Unaria: A != Azul)
print("Paso 1: Aplicar Consistencia de Nodo (A != Azul)")
if 'Azul' in DOMINIOS['A']:
    DOMINIOS['A'].remove('Azul')
    print(f"Dominio A podado a: {DOMINIOS['A']}")

# 2. Aplicar AC-3 (Consistencia de Arco)
print("\nPaso 2: Aplicar AC-3 para propagar el cambio de A")
consistente = AC3(DOMINIOS)

print("-" * 50)
if consistente:
    print("AC-3 finalizado. Consistencia de Arco alcanzada.")
    print("Dominios Resultantes después de la Propagación:")
    for var, dom in DOMINIOS.items():
        print(f"  {var}: {dom}")
else:
    print("El CSP no tiene solución.")