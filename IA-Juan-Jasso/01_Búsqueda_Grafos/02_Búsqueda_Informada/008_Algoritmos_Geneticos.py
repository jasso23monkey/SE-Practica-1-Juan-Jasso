import random

# --- 1. CONFIGURACIÓN ---
TAMAÑO_CROMOSOMA = 8  # 8 bits: la solución es "11111111"
TAMAÑO_POBLACION = 5
MAX_GENERACIONES = 15
TASA_MUTACION = 0.05  # 1% de probabilidad de que un bit mute

# --- 2. FUNCIÓN DE APTITUD (Fitness) ---
def calcular_aptitud(cromosoma):
    """Calcula la aptitud (fitness): el número de unos en la cadena."""
    # La aptitud es simplemente la suma de los bits. Máximo 8.
    return sum(cromosoma)

# --- 3. INICIALIZACIÓN ---
def inicializar_poblacion(tamano_poblacion, tamano_cromosoma):
    """Crea una población inicial de cromosomas binarios aleatorios."""
    poblacion = []
    for _ in range(tamano_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(tamano_cromosoma)]
        poblacion.append(cromosoma)
    return poblacion

# --- 4. SELECCIÓN (Ruleta Simplificada) ---
def seleccionar_padres(poblacion, aptitudes):
    """Selecciona dos padres con probabilidad basada en su aptitud."""
    # Ruleta: Crea una lista de toda la población, repitiendo individuos según su aptitud.
    padres_candidatos = []
    for i, aptitud in enumerate(aptitudes):
        padres_candidatos.extend([poblacion[i]] * aptitud) # Repite el cromosoma 'aptitud' veces

    # Si la lista está vacía (aptitud 0 para todos), regresa la población original
    if not padres_candidatos:
        return random.choices(poblacion, k=2) 
        
    # Elige dos padres de forma aleatoria de la lista de candidatos
    padre1 = random.choice(padres_candidatos)
    padre2 = random.choice(padres_candidatos)
    return padre1, padre2

# --- 5. CRUCE (Crossover de un punto) ---
def cruzar(padre1, padre2):
    """Combina dos padres en un punto de corte aleatorio."""
    punto_corte = random.randint(1, TAMAÑO_CROMOSOMA - 1)
    
    # Hereda la primera parte del padre1 y la segunda parte del padre2
    hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
    hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
    
    return hijo1, hijo2

# --- 6. MUTACIÓN ---
def mutar(cromosoma, tasa_mutacion):
    """Invierte un bit con una pequeña probabilidad."""
    for i in range(len(cromosoma)):
        if random.random() < tasa_mutacion:
            # Invierte el bit (0 se vuelve 1, 1 se vuelve 0)
            cromosoma[i] = 1 - cromosoma[i]
    return cromosoma

# ===============================================
# --- ALGORITMO GENÉTICO PRINCIPAL ---
# ===============================================

poblacion_actual = inicializar_poblacion(TAMAÑO_POBLACION, TAMAÑO_CROMOSOMA)
mejor_aptitud_global = 0

print("--- Algoritmo Genético (Meta: 8 unos) ---")

for generacion in range(1, MAX_GENERACIONES + 1):
    aptitudes = [calcular_aptitud(c) for c in poblacion_actual]
    nueva_poblacion = []
    
    # Elitismo: Mantener el mejor individuo de la generación pasada
    mejor_indice = aptitudes.index(max(aptitudes))
    nueva_poblacion.append(poblacion_actual[mejor_indice])
    
    mejor_aptitud_global = max(mejor_aptitud_global, aptitudes[mejor_indice])
    
    # Llenar el resto de la nueva población (TAMAÑO_POBLACION - 1)
    for _ in range(TAMAÑO_POBLACION - 1):
        # 1. Selección
        padre1, padre2 = seleccionar_padres(poblacion_actual, aptitudes)
        
        # 2. Cruce
        hijo1, _ = cruzar(padre1, padre2)
        
        # 3. Mutación
        hijo_mutado = mutar(hijo1, TASA_MUTACION)
        
        nueva_poblacion.append(hijo_mutado)

    poblacion_actual = nueva_poblacion
    
    aptitud_media = sum(aptitudes) / len(aptitudes)
    print(f"Gen {generacion:02d}: Aptitud Máx: {max(aptitudes)} | Aptitud Media: {aptitud_media:.2f}")

    if mejor_aptitud_global == TAMAÑO_CROMOSOMA:
        break

# --- RESULTADOS FINALES ---
mejor_solucion = [c for c in poblacion_actual if calcular_aptitud(c) == mejor_aptitud_global][0]

print("-" * 40)
print(f"Búsqueda finalizada en la Generación {generacion}.")
print(f"Mejor Solución Encontrada: {''.join(map(str, mejor_solucion))} (Aptitud: {mejor_aptitud_global})")