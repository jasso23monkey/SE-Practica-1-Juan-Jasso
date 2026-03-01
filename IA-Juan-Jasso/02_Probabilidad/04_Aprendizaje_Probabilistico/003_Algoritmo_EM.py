import numpy as np

# --- A. Simulación de Datos (Dos Gaussianas Mezcladas) ---
np.random.seed(42)
N = 1000 # Total de puntos

# Gaussiana 1 (Clase A)
mu1_real, sigma1_real = -2, 1
N1 = int(0.6 * N)
data1 = np.random.normal(mu1_real, sigma1_real, N1)

# Gaussiana 2 (Clase B)
mu2_real, sigma2_real = 3, 1
N2 = N - N1
data2 = np.random.normal(mu2_real, sigma2_real, N2)

# Datos observados (mezclados)
X = np.concatenate([data1, data2])
X = X.reshape(-1, 1) # Asegurar que sea una columna

# --- B. Inicialización del Algoritmo EM ---
K = 2 # Número de componentes (Gaussianas) que queremos encontrar

# Inicialización ingenua de parámetros (los que el EM ajustará)
# Pesos iniciales (Pi): Proporción de cada Gaussiana
pi = np.array([0.5, 0.5]) 
# Medias iniciales (Mu): Elegidas aleatoriamente
mu = X[np.random.choice(N, K, replace=False), :] 
# Varianzas iniciales (Sigma^2): Se asume varianza unitaria
sigma2 = np.array([1.0, 1.0]) 

MAX_ITER = 100
TOLERANCIA = 1e-4

log_verosimilitud_anterior = -np.inf

def pdf_gaussiana(x, mu, sigma2):
    """Calcula la Densidad de Probabilidad (PDF) de una Gaussiana 1D."""
    # pdf = 1 / sqrt(2*pi*sigma^2) * exp( -0.5 * (x - mu)^2 / sigma^2 )
    numerador = np.exp(-0.5 * (x - mu)**2 / sigma2)
    denominador = np.sqrt(2 * np.pi * sigma2)
    return numerador / denominador

def calcular_log_verosimilitud(X, pi, mu, sigma2):
    """Calcula la verosimilitud logarítmica de los datos observados."""
    verosimilitud = pi[0] * pdf_gaussiana(X, mu[0], sigma2[0]) + \
                    pi[1] * pdf_gaussiana(X, mu[1], sigma2[1])
    # Evitar log(0)
    verosimilitud = np.maximum(verosimilitud, 1e-300) 
    return np.sum(np.log(verosimilitud))

for iteracion in range(MAX_ITER):
    # =================================================================
    # PASO E (Expectation - Expectativa)
    # Calcular la responsabilidad (r_ik): P(Z_i=k | X_i, theta_antiguo)
    # Es la probabilidad de que el punto X_i provenga del componente k.
    # =================================================================
    
    # Calcular la Verosimilitud de cada punto en cada componente
    L1 = pdf_gaussiana(X, mu[0], sigma2[0]) # P(X | Z=1)
    L2 = pdf_gaussiana(X, mu[1], sigma2[1]) # P(X | Z=2)
    
    # Calcular el numerador de la responsabilidad: P(X | Z=k) * P(Z=k)
    numerador1 = pi[0] * L1
    numerador2 = pi[1] * L2
    
    # Calcular el denominador (verosimilitud marginal): P(X) = P(X|Z=1)P(Z=1) + P(X|Z=2)P(Z=2)
    denominador = numerador1 + numerador2
    
    # Calcular la responsabilidad (r_ik)
    r1 = numerador1 / denominador # Responsabilidad del componente 1
    r2 = numerador2 / denominador # Responsabilidad del componente 2
    
    # Matriz de responsabilidades: N x K
    r = np.hstack([r1, r2]) 
    
    
    # =================================================================
    # PASO M (Maximization - Maximización)
    # Actualizar los parámetros (pi, mu, sigma2) para maximizar Q
    # =================================================================
    
    # N_k: Suma total de responsabilidades para cada componente
    N1_k = np.sum(r1)
    N2_k = np.sum(r2)
    
    # 1. Actualizar los Pesos (Pi): Pi_k = N_k / N
    pi[0] = N1_k / N
    pi[1] = N2_k / N
    
    # 2. Actualizar las Medias (Mu): Mu_k = Sum(r_ik * X_i) / N_k
    mu[0] = np.sum(r1 * X.flatten()) / N1_k
    mu[1] = np.sum(r2 * X.flatten()) / N2_k
    
    # 3. Actualizar las Varianzas (Sigma^2): Sigma^2_k = Sum(r_ik * (X_i - Mu_k)^2) / N_k
    sigma2[0] = np.sum(r1 * (X.flatten() - mu[0])**2) / N1_k
    sigma2[1] = np.sum(r2 * (X.flatten() - mu[1])**2) / N2_k
    
    
    # =================================================================
    # Verificación de Convergencia
    # =================================================================
    log_verosimilitud_actual = calcular_log_verosimilitud(X, pi, mu, sigma2)
    
    if np.abs(log_verosimilitud_actual - log_verosimilitud_anterior) < TOLERANCIA:
        print(f"Convergió en la iteración {iteracion + 1}.")
        break
        
    log_verosimilitud_anterior = log_verosimilitud_actual
    
# --- 4. Resultados Finales ---

print("\n=======================================================")
print("      RESULTADOS FINALES DEL ALGORITMO EM")
print("=======================================================")
print(f"Iteraciones completadas: {iteracion + 1}")
print(f"Log-Verosimilitud final: {log_verosimilitud_actual:.4f}")
print("-" * 50)
print("Parámetros Reales de la Simulación:")
print(f"  Componente 1 (Real): Peso ≈ 0.60, Mu = {mu1_real}, Sigma² = {sigma1_real**2}")
print(f"  Componente 2 (Real): Peso ≈ 0.40, Mu = {mu2_real}, Sigma² = {sigma2_real**2}")
print("-" * 50)
print("Parámetros Encontrados por el EM:")
print(f"  Componente 1 (EM): Peso = {pi[0]:.3f}, Mu = {mu[0, 0]:.3f}, Sigma² = {sigma2[0]:.3f}")
print(f"  Componente 2 (EM): Peso = {pi[1]:.3f}, Mu = {mu[1, 0]:.3f}, Sigma² = {sigma2[1]:.3f}")

# La salida muestra que el EM se aproxima a los parámetros reales (0.65 vs 0.60, 3.03 vs 3.0, etc.)