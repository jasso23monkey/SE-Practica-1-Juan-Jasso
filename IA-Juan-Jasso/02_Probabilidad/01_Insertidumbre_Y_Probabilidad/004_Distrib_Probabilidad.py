import numpy as np
import matplotlib.pyplot as plt

# --- 1. FUNCIÓN DE DENSIDAD DE PROBABILIDAD (FDP) GAUSSIANA ---

def normal_pdf(x, mu, sigma):
    """Calcula la Función de Densidad de Probabilidad de una Distribución Normal."""
    
    # Término de normalización (el denominador)
    denominador = sigma * np.sqrt(2 * np.pi)
    
    # Término exponencial
    exponente = -0.5 * ((x - mu) / sigma)**2
    
    # Resultado de la FDP
    return np.exp(exponente) / denominador


# --- 2. DATOS DE ENTRADA Y ESTIMACIÓN DE PARÁMETROS (MLE) ---

# Muestra de temperaturas corporales
datos_temperatura = np.array([37.05, 36.88, 37.15, 36.92, 37.01, 37.20, 36.75, 37.08, 36.95, 37.10, 
                             37.02, 36.85, 37.18, 36.95, 37.00, 37.15, 36.80, 37.05, 36.90, 37.12,
                             37.00, 36.99, 37.01, 37.00, 36.98, 37.03, 36.97, 37.04, 36.96, 37.02,
                             37.00, 37.05, 37.00, 36.95, 37.05, 36.90, 37.10, 36.85, 37.15, 37.00])


# Estimación de la Media (μ) - Promedio
mu_estimada = np.mean(datos_temperatura)

# Estimación de la Desviación Estándar (σ)
sigma_estimada = np.std(datos_temperatura)


# --- 3. CREACIÓN Y VISUALIZACIÓN DE LA DISTRIBUCIÓN ---

# Generar puntos X para dibujar la curva
x_min = np.min(datos_temperatura) - 0.1
x_max = np.max(datos_temperatura) + 0.1
x = np.linspace(x_min, x_max, 100)

# Calcular la FDP utilizando nuestra función personalizada
fdp_estimada = normal_pdf(x, mu_estimada, sigma_estimada)


plt.figure(figsize=(10, 6))

# Dibujar el histograma de los datos reales
plt.hist(datos_temperatura, bins=10, density=True, alpha=0.6, color='skyblue', label='Frecuencia Empírica (Datos Reales)')

# Dibujar la FDP de la Distribución Normal estimada
plt.plot(x, fdp_estimada, 'r-', lw=2, label=f'Distribución Normal Estimada\n($\mu$={mu_estimada:.4f}, $\sigma$={sigma_estimada:.4f})')

plt.title('Estimación de la Distribución de Probabilidad (Distribución Normal)')
plt.xlabel('Temperatura Corporal (°C)')
plt.ylabel('Densidad de Probabilidad')
plt.axvline(mu_estimada, color='gray', linestyle='dashed', linewidth=1)
plt.legend()
plt.grid(axis='y', alpha=0.5)
plt.show()

print("--- Estimación de la Distribución de Probabilidad (Sin SciPy) ---")
print(f"Media Estimada (μ): {mu_estimada:.4f} °C")
print(f"Desviación Estándar Estimada (σ): {sigma_estimada:.4f} °C")