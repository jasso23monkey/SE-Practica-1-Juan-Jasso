import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de Parámetros ---
N_PARTICULAS = 1000  # Número de partículas
T_PASOS = 50         # Número de pasos de tiempo
DT = 1.0             # Intervalo de tiempo
VELOCIDAD_REAL = 0.5 # Velocidad constante real del objeto
VARIANZA_PROCESO = 0.1 # Varianza del ruido del proceso (modelo de movimiento)
ANCHO_RUIDO_MEDICION = 2.0 # Amplitud del ruido de medición (uniforme: [-2.0, 2.0])

# --- 2. Modelos de Transición y Emisión ---

# Modelo de Transición (Función de Predicción)
def predecir_movimiento(particulas):
    """X_t = X_{t-1} + V * dt + Ruido Gaussiano (Asumimos modelo simple)"""
    # El ruido es Gaussiano para la transición (lo más común)
    ruido_proceso = np.random.normal(0, np.sqrt(VARIANZA_PROCESO), N_PARTICULAS)
    return particulas + VELOCIDAD_REAL * DT + ruido_proceso

# Modelo de Emisión (Verosimilitud) - Ruido Uniforme NO GAUSSIANO
def calcular_verosimilitud(medicion, particulas):
    """P(E_t | X_t): Probabilidad de la medición dada la partícula."""
    # Ruido Uniforme: Si la partícula está dentro del rango de ruido de la medición,
    # la probabilidad es constante (1 / Ancho); sino, es 0.
    
    diferencia = np.abs(medicion - particulas)
    
    # La verosimilitud es P(Z_t | X_t)
    verosimilitud = np.where(
        diferencia <= ANCHO_RUIDO_MEDICION,
        1.0 / (2.0 * ANCHO_RUIDO_MEDICION), # Densidad constante 
        0.0 # Fuera del rango de ruido
    )
    return verosimilitud

# --- 3. Función de Remuestreo (Importancia) ---
def remuestreo(particulas, pesos):
    """
    Remuestrea las partículas basadas en sus pesos (Sampling Importance Resampling - SIR).
    """
    # Normalizar los pesos para que sumen 1
    pesos /= np.sum(pesos)
    
    # Índices seleccionados (más probable que se seleccionen los de mayor peso)
    indices = np.random.choice(
        N_PARTICULAS, 
        size=N_PARTICULAS, 
        p=pesos 
    )
    
    # Crear el nuevo conjunto de partículas (duplicación y eliminación)
    particulas_remuestreadas = particulas[indices]
    
    # Resetear pesos a uniforme
    nuevos_pesos = np.ones(N_PARTICULAS) / N_PARTICULAS
    
    return particulas_remuestreadas, nuevos_pesos

# --- SIMULACIÓN DE DATOS REALES ---
posicion_real = np.zeros(T_PASOS)
mediciones = np.zeros(T_PASOS)

# Generar la trayectoria real y las mediciones ruidosas (uniforme)
for t in range(1, T_PASOS):
    posicion_real[t] = posicion_real[t-1] + VELOCIDAD_REAL * DT
    # Ruido de medición uniforme: Uniforme[-A, A]
    mediciones[t] = posicion_real[t] + np.random.uniform(
        -ANCHO_RUIDO_MEDICION, ANCHO_RUIDO_MEDICION
    )


# --- INICIALIZACIÓN DEL FILTRO ---
# Partículas iniciales uniformemente distribuidas
particulas = np.random.uniform(-5, 5, N_PARTICULAS) 
pesos = np.ones(N_PARTICULAS) / N_PARTICULAS
posiciones_estimadas = []


# --- BUCLE DEL FILTRO DE PARTÍCULAS ---
for t in range(T_PASOS):
    
    # 1. PREDICCIÓN (Propagar partículas)
    if t > 0:
        particulas = predecir_movimiento(particulas)
    
    # 2. ACTUALIZACIÓN (Ponderar)
    medicion_actual = mediciones[t]
    
    # Calcular verosimilitud P(E_t | X_t)
    verosimilitud = calcular_verosimilitud(medicion_actual, particulas)
    
    # Actualizar pesos: w_t = w_{t-1} * P(E_t | X_t)
    pesos *= verosimilitud
    
    # Normalizar los pesos antes de calcular la estimación
    if np.sum(pesos) > 0:
        pesos_normalizados = pesos / np.sum(pesos)
    else:
        # Manejar caso degenerado: si todos los pesos son cero
        pesos_normalizados = np.ones(N_PARTICULAS) / N_PARTICULAS

    # Estimación del estado (media ponderada)
    estimacion = np.sum(particulas * pesos_normalizados)
    posiciones_estimadas.append(estimacion)

    # 3. REMUESTREO (Evitar la Degeneración)
    # Solo remuestrear si la distribución está muy degenerada (opcional: usar Neff)
    particulas, pesos = remuestreo(particulas, pesos)


# --- 5. Visualización ---
plt.figure(figsize=(12, 6))
plt.plot(posicion_real, label='Posición Real (Oculta)', color='green', linewidth=3, alpha=0.7)
plt.scatter(range(T_PASOS), mediciones, label='Mediciones Ruidosas (Ruido Uniforme)', color='red', alpha=0.5, marker='.')
plt.plot(posiciones_estimadas, label='Estimación del Filtro de Partículas', color='blue', linestyle='--', linewidth=2)

plt.title(f'Filtrado de Partículas (PF) con {N_PARTICULAS} Partículas')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()