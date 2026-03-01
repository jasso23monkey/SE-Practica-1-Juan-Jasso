import random

# Definición de los estados y la Matriz de Transición
ESTADOS = ['Soleado', 'Nublado', 'Lluvioso']

# Matriz T: T[i][j] = P(j | i)
# i (fila) = estado actual, j (columna) = estado siguiente
MATRIZ_TRANSICION = {
    'Soleado': {'Soleado': 0.8, 'Nublado': 0.15, 'Lluvioso': 0.05},
    'Nublado': {'Soleado': 0.2, 'Nublado': 0.6, 'Lluvioso': 0.2},
    'Lluvioso': {'Soleado': 0.1, 'Nublado': 0.3, 'Lluvioso': 0.6}
}

def siguiente_estado(estado_actual):
    """
    Selecciona el siguiente estado basándose en la Matriz de Transición 
    y el estado actual, simulando la Hipótesis de Markov.
    """
    probabilidades = MATRIZ_TRANSICION[estado_actual]
    
    # Crea una lista de estados y sus probabilidades
    estados_futuros = list(probabilidades.keys())
    probs = list(probabilidades.values())
    
    # random.choices selecciona un elemento basado en los pesos (probabilidades)
    # k=1 significa que selecciona un solo elemento.
    return random.choices(estados_futuros, weights=probs, k=1)[0]

def simular_cadena_markov(dias, estado_inicial):
    """Simula la secuencia de estados de la Cadena de Markov."""
    historia = [estado_inicial]
    estado_actual = estado_inicial
    
    print(f"--- Simulación de {dias} días (Inicio: {estado_inicial}) ---")
    
    for dia in range(1, dias):
        # El cálculo del siguiente estado ignora toda la historia
        # antes del estado_actual. Esto es la Hipótesis de Markov.
        estado_siguiente = siguiente_estado(estado_actual)
        
        historia.append(estado_siguiente)
        
        # Muestra cómo el futuro depende solo del presente
        if dia < 5:
            print(f"Día {dia}: {estado_actual} -> Día {dia+1}: {estado_siguiente}")
            
        estado_actual = estado_siguiente
        
    return historia

# --- Ejecución del Ejemplo ---

NUM_DIAS = 20
INICIO = 'Soleado'
historial_clima = simular_cadena_markov(NUM_DIAS, INICIO)

print("\n" + "="*50)
print(f"Secuencia Completa (días 1 a {NUM_DIAS}):")
print(historial_clima)
