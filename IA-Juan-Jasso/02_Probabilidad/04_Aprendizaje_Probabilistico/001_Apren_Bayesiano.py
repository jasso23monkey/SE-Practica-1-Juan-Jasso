import numpy as np
import matplotlib.pyplot as plt
import math # Se usará para el factorial (que reemplaza a Gamma)

# --- Función Auxiliar para la PDF de Beta (Sin Scipy) ---
def factorial(n):
    """Calcula el factorial de n. Usado para reemplazar Gamma(n+1) = n!"""
    if n < 0:
        raise ValueError("Factorial no definido para números negativos.")
    return math.factorial(int(n))

def beta_pdf_sin_scipy(theta, a, b):
    """
    Calcula la Función de Densidad de Probabilidad (PDF) de la distribución Beta.
    Asume que a y b son enteros > 0 (cierto en este ejemplo).
    """
    # Usamos la definición: Beta(a, b) = (a-1)! * (b-1)! / (a+b-1)!
    
    # 1. Coeficiente de Normalización (1 / B(a,b))
    try:
        # 1 / B(a,b) = (a+b-1)! / ((a-1)! * (b-1)!)
        normalizacion = factorial(a + b - 1) / (factorial(a - 1) * factorial(b - 1))
    except ValueError:
        # Manejo de casos límite si a=1 o b=1 (factorial de 0 es 1)
        if a == 1 and b == 1:
            normalizacion = 1.0 # Beta(1,1) es la distribución Uniforme
        else:
            # En un entorno real, se usaría math.gamma
            normalizacion = 1.0 # Aproximación simplificada para evitar errores complejos
    
    # 2. PDF
    # P(theta) = Normalización * theta^(a-1) * (1-theta)^(b-1)
    
    # El uso de np.power asegura que theta puede ser un array de NumPy.
    return normalizacion * np.power(theta, a - 1) * np.power(1 - theta, b - 1)

# --- 1. Definición de la Previa (Creencia Inicial) ---
PRIOR_A = 1
PRIOR_B = 1

# --- 2. Simulación de la Evidencia (Datos) ---
LANZAMIENTOS = 100
PROB_REAL_MONEDA = 0.65 

np.random.seed(42)
resultados = np.random.binomial(n=1, p=PROB_REAL_MONEDA, size=LANZAMIENTOS)

EXITOS_OBSERVADOS = np.sum(resultados)
FRACASOS_OBSERVADOS = LANZAMIENTOS - EXITOS_OBSERVADOS

print(f"Lanzamientos: {LANZAMIENTOS}")
print(f"Éxitos observados: {EXITOS_OBSERVADOS}")
print("-" * 40)


# --- 3. Cálculo de la Posterior (Actualización Bayesiana) ---
POSTERIOR_A = PRIOR_A + EXITOS_OBSERVADOS
POSTERIOR_B = PRIOR_B + FRACASOS_OBSERVADOS

print("Parámetros de la Distribución Posterior:")
print(f"Alpha (a): {POSTERIOR_A}")
print(f"Beta (b): {POSTERIOR_B}")
print("-" * 40)


# --- 4. Predicción y Visualización ---

# Rango de posibles valores para la probabilidad de éxito (theta)
theta_values = np.linspace(0.01, 0.99, 500) # Evitar 0 y 1 para simplificar el cálculo de PDF

# Distribución Previa usando nuestra función auxiliar
prior_pdf = beta_pdf_sin_scipy(theta_values, PRIOR_A, PRIOR_B)

# Distribución Posterior usando nuestra función auxiliar
posterior_pdf = beta_pdf_sin_scipy(theta_values, POSTERIOR_A, POSTERIOR_B)

# Media de la Posterior (Mejor estimación bayesiana de theta)
media_posterior = POSTERIOR_A / (POSTERIOR_A + POSTERIOR_B)


plt.figure(figsize=(10, 6))
plt.plot(theta_values, prior_pdf, label=f'Distribución Previa (Beta({PRIOR_A}, {PRIOR_B}))', 
         color='gray', linestyle='--')
plt.plot(theta_values, posterior_pdf, label=f'Distribución Posterior (Beta({POSTERIOR_A}, {POSTERIOR_B}))', 
         color='blue', linewidth=3)
plt.axvline(PROB_REAL_MONEDA, color='red', linestyle=':', label=f'Probabilidad Real ({PROB_REAL_MONEDA})')
plt.axvline(media_posterior, color='green', linestyle='-', label=f'Estimación Bayesiana (Media: {media_posterior:.3f})')

plt.title('Aprendizaje Bayesiano: Estimación de la Probabilidad de una Moneda')
plt.xlabel('Probabilidad de Éxito (θ)')
plt.ylabel('Densidad de Probabilidad')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"La estimación bayesiana para la probabilidad de éxito de la moneda es: {media_posterior:.3f}")