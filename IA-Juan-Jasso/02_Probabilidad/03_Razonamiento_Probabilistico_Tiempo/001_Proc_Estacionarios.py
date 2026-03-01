import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros de la simulación ---
N = 500         # Número de puntos en la serie temporal
c = 0.0         # Media (intercepto), lo fijamos en cero
phi = 0.5       # Coeficiente AR(1). Estacionario porque |phi| < 1
sigma_e = 1.0   # Desviación estándar del ruido

# --- 1. Generación del Ruido Blanco ---
# El ruido es la parte estocástica (aleatoria) del proceso.
ruido = np.random.normal(loc=0, scale=sigma_e, size=N)

# --- 2. Generación del Proceso AR(1) Estacionario ---
# Inicializamos la serie temporal
X = np.zeros(N)

# Asignamos un valor inicial arbitrario
X[0] = ruido[0] 

# Generamos la serie temporal paso a paso
for t in range(1, N):
    # Xt = c + phi * X_{t-1} + epsilon_t
    X[t] = c + phi * X[t-1] + ruido[t]

# --- 3. Verificación de la Estacionariedad ---
# En un proceso estacionario, la media y la varianza son constantes.

# Calculamos la media y varianza teórica del AR(1) estacionario
# Media teórica (mu) = c / (1 - phi)
media_teorica = c / (1 - phi) 
# Varianza teórica (gamma_0) = sigma_e^2 / (1 - phi^2)
varianza_teorica = (sigma_e**2) / (1 - phi**2)

print("--- Proceso Estacionario AR(1) ---")
print(f"Parámetro phi: {phi}")
print(f"Media teórica: {media_teorica:.3f}")
print(f"Varianza teórica: {varianza_teorica:.3f}")
print("-" * 40)
print(f"Media muestral: {np.mean(X):.3f}")
print(f"Varianza muestral: {np.var(X):.3f}")

# --- 4. Visualización ---

plt.figure(figsize=(12, 5))
plt.plot(X, label=f'Serie Estacionaria AR(1) con $\phi$={phi}', color='darkblue')
# Línea de la media para demostrar que es constante
plt.axhline(y=media_teorica, color='red', linestyle='--', label='Media Teórica')
plt.title('Ejemplo de un Proceso Estacionario en Sentido Débil')
plt.xlabel('Tiempo')
plt.ylabel('Valores de $X_t$')
plt.legend()
plt.grid(True, alpha=0.5)
plt.show()