import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import math 

# --- 1. Preparación de Datos y Conteo (Mismo código de antes) ---

# Mensajes de correo y etiquetas
mensajes = [
    "gana dinero facil rapido haz clic aqui", 
    "reunion manana en sala 3",              
    "urge premio oferta limitada",           
    "confirma cuenta bancaria ahora",         
    "adjunto informe trimestral solicitado",  
    "promocion exclusiva no te lo pierdas",  
    "tienes tiempo para hablar",             
    "suscribete bono 1 millon",               
    "donde dejamos las llaves del coche"      
]
etiquetas = ['spam', 'ham', 'spam', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
vocabulario = set(" ".join(mensajes).split())

# Conteo de clases y palabras (Diccionarios)
conteo_clases = defaultdict(int)
for etiqueta in etiquetas:
    conteo_clases[etiqueta] += 1
    
conteo_palabras_por_clase = defaultdict(lambda: defaultdict(int))
conteo_total_palabras_por_clase = defaultdict(int)

for mensaje, etiqueta in zip(mensajes, etiquetas):
    palabras = mensaje.split()
    for palabra in palabras:
        conteo_palabras_por_clase[etiqueta][palabra] += 1
        conteo_total_palabras_por_clase[etiqueta] += 1

# Probabilidades Previas (P(Clase))
total_documentos = len(mensajes)
P_spam = conteo_clases['spam'] / total_documentos
P_ham = conteo_clases['ham'] / total_documentos

# Suavizado de Laplace (Alpha = 1)
ALPHA = 1

# --- 2. Funciones Auxiliares (Mismo código de antes) ---

def calcular_probabilidad_palabra_dada_clase(palabra, clase, conteo_palabras, total_palabras_clase, vocab_size):
    """Calcula P(Palabra | Clase) con suavizado de Laplace."""
    conteo_palabra_en_clase = conteo_palabras[clase].get(palabra, 0)
    total_palabras_en_clase = total_palabras_clase[clase]
    prob = (conteo_palabra_en_clase + ALPHA) / (total_palabras_en_clase + ALPHA * vocab_size)
    return prob

def clasificar_naive_bayes(mensaje, P_spam, P_ham, conteo_palabras, total_palabras_clase, vocabulario):
    """Clasifica un nuevo mensaje y retorna las probabilidades logarítmicas."""
    palabras = mensaje.split()
    vocab_size = len(vocabulario)
    
    # log(P(Spam | E)) = log(P(Spam)) + SUM [log(P(e_i | Spam))]
    log_prob_spam = np.log(P_spam)
    for palabra in palabras:
        prob_palabra_spam = calcular_probabilidad_palabra_dada_clase(palabra, 'spam', conteo_palabras, total_palabras_clase, vocab_size)
        log_prob_spam += np.log(prob_palabra_spam)

    # log(P(Ham | E))
    log_prob_ham = np.log(P_ham)
    for palabra in palabras:
        prob_palabra_ham = calcular_probabilidad_palabra_dada_clase(palabra, 'ham', conteo_palabras, total_palabras_clase, vocab_size)
        log_prob_ham += np.log(prob_palabra_ham)
        
    pred = 'spam' if log_prob_spam > log_prob_ham else 'ham'
        
    return pred, log_prob_spam, log_prob_ham

# --- 3. Prueba y Visualización ---

# MENSAJE DE PRUEBA que queremos graficar:
MENSAJE_A_GRAFICAR = "ganaste viaje gratis reclama ahora" 

# Clasificar el mensaje para obtener los valores logarítmicos
pred, log_spam, log_ham = clasificar_naive_bayes(
    MENSAJE_A_GRAFICAR, P_spam, P_ham, conteo_palabras_por_clase, conteo_total_palabras_por_clase, vocabulario
)

# Imprimir el resultado de la clasificación
print("==============================================")
print("     CLASIFICADOR NAÏVE BAYES (DECISIÓN)")
print("==============================================")
print(f"Mensaje: '{MENSAJE_A_GRAFICAR}'")
print(f"Predicción: {pred.upper()}")
print(f"Log P(Spam | Mensaje): {log_spam:.4f}")
print(f"Log P(Ham | Mensaje): {log_ham:.4f}")
print("-" * 45)

# --- Generar la Gráfica de Barras ---

etiquetas_grafico = ['Log P(Spam)', 'Log P(Ham)']
valores_log = [log_spam, log_ham]

plt.figure(figsize=(7, 5))
plt.bar(etiquetas_grafico, valores_log, 
        color=['red' if pred == 'spam' else 'gray', 'blue' if pred == 'ham' else 'gray'],
        width=0.4)

plt.axhline(0, color='black', linewidth=0.5) # Línea en y=0
plt.title(f'Decisión Naïve Bayes para: "{MENSAJE_A_GRAFICAR}"')
plt.ylabel('Probabilidad Logarítmica Posterior')
plt.text(0, log_spam, f'{log_spam:.2f}', ha='center', va='bottom', fontsize=10)
plt.text(1, log_ham, f'{log_ham:.2f}', ha='center', va='bottom', fontsize=10)

plt.show()