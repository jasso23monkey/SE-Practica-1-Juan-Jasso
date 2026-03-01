import numpy as np
import matplotlib.pyplot as plt

# --- A. Simulación de Datos Linealmente Separables ---
np.random.seed(42)

# Clase A: Etiqueta y = 1 (rojo)
X_A = np.random.normal(loc=[1, 2], scale=0.5, size=(20, 2))
y_A = np.ones(20)

# Clase B: Etiqueta y = -1 (azul)
X_B = np.random.normal(loc=[4, 4], scale=0.5, size=(20, 2))
y_B = -np.ones(20)

X = np.vstack([X_A, X_B])
y = np.hstack([y_A, y_B])

# --- B. Identificación Conceptual de Vectores Soporte ---
# En un SVM real, un optimizador encuentra estos puntos. 
# Aquí, los elegimos manualmente cerca del límite imaginario.

# Vectores soporte (Vs) definen el margen
# Vs1 (Clase A): Punto de la clase A más cercano al límite
Vs1 = np.array([1.5, 2.5]) 

# Vs2 (Clase B): Punto de la clase B más cercano al límite
Vs2 = np.array([3.5, 3.0]) 
Vs3 = np.array([4.0, 3.5])

# Para este ejemplo, usaremos dos vectores soporte para simplificar el cálculo conceptual
Vs = np.vstack([Vs1, Vs2])

print(f"Número total de puntos de datos: {len(X)}")
print(f"Número de vectores soporte clave usados: {len(Vs)}")

# --- C. Definición del Kernel ---

def kernel_lineal(x1, x2):
    """
    K(x1, x2) = x1 . x2 (Producto escalar).
    Este es el kernel más simple.
    """
    return np.dot(x1, x2)

# CÁLCULO CONCEPTUAL DE W y B BASADO EN LA GEOMETRÍA DEL MARGEN
# W apunta desde Vs1 a Vs2, perpendicular al hiperplano separador.

# Punto medio entre los dos vectores soporte
punto_medio = (Vs1 + Vs2) / 2

# El vector normal (w) al hiperplano es perpendicular al margen.
# Para simplificar, W es el vector de diferencia entre los Vs
# En SVM, W es perpendicular al segmento Vs1-Vs2
w_temp = Vs2 - Vs1 
w = np.array([-w_temp[1], w_temp[0]]) # Vector perpendicular a w_temp

# Normalizar W para tener una unidad de escala limpia (opcional, pero buena práctica)
w = w / np.linalg.norm(w)

# Calcular 'b' (sesgo) para que el hiperplano pase por el punto medio
# El hiperplano pasa por el centro del margen (punto_medio).
# w . punto_medio + b = 0  => b = - (w . punto_medio)
b = -kernel_lineal(w, punto_medio)

# --- D. Visualización con Matplotlib ---

plt.figure(figsize=(8, 6))

# 1. Graficar los datos
plt.scatter(X_A[:, 0], X_A[:, 1], c='red', label='Clase A (y=1)', marker='o', alpha=0.6)
plt.scatter(X_B[:, 0], X_B[:, 1], c='blue', label='Clase B (y=-1)', marker='s', alpha=0.6)

# 2. Graficar los Vectores Soporte (resaltados)
plt.scatter(Vs[:, 0], Vs[:, 1], s=300, facecolors='none', edgecolors='k', linewidth=2, label='Vectores Soporte')

# 3. Dibujar el Hiperplano Óptimo (Recta de Separación)

# Generar puntos x para dibujar la recta: x2 = (-w1*x1 - b) / w2
x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
x1_values = np.linspace(x1_min, x1_max, 100)

# Línea del Hiperplano: w[0]*x1 + w[1]*x2 + b = 0
x2_hiperplano = (-w[0] * x1_values - b) / w[1]

# Líneas del Margen (a distancia 1 del hiperplano)
# w . x + b = 1  => x2 = (-w1*x1 - b + 1) / w2
x2_margen_superior = (-w[0] * x1_values - b + 1) / w[1] 
# w . x + b = -1 => x2 = (-w1*x1 - b - 1) / w2
x2_margen_inferior = (-w[0] * x1_values - b - 1) / w[1] 

# Dibujar las líneas
plt.plot(x1_values, x2_hiperplano, 'k-', label='Hiperplano Separador (w⋅x + b = 0)', linewidth=2)
plt.plot(x1_values, x2_margen_superior, 'k--', label='Margen', linewidth=1)
plt.plot(x1_values, x2_margen_inferior, 'k--', linewidth=1)
plt.fill_between(x1_values, x2_margen_inferior, x2_margen_superior, color='gray', alpha=0.1, label='Margen')


plt.title('SVM Lineal con Kernel Lineal')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.axis('equal') # Mantener la escala de los ejes igual
plt.legend(loc='lower left')
plt.grid(True, linestyle=':', alpha=0.5)
plt.show()

print("\n=============================================")
print("  PARÁMETROS DEL HIPERPLANO ENCONTRADO")
print("=============================================")
print(f"Vector de Pesos (w): {w}")
print(f"Sesgo (b): {b:.3f}")
print(f"Ecuación del Hiperplano: {w[0]:.3f}x₁ + {w[1]:.3f}x₂ + {b:.3f} = 0")