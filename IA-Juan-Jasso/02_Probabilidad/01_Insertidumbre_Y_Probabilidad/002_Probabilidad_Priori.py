# --- Probabilidades a Priori (P(C)) ---
P_Spam = 0.4
P_NoSpam = 0.6

# --- Verosimilitudes (P(E|C)) ---
P_Desc_dado_Spam = 0.7
P_Desc_dado_NoSpam = 0.1

# 1. Calcular el Denominador P(E) = P(E|Spam)*P(Spam) + P(E|NoSpam)*P(NoSpam)
P_Desc = (P_Desc_dado_Spam * P_Spam) + (P_Desc_dado_NoSpam * P_NoSpam)
# P_Desc = (0.7 * 0.4) + (0.1 * 0.6) = 0.28 + 0.06 = 0.34

# 2. Calcular la Probabilidad a Posteriori (P(C|E))
P_Spam_dado_Desc = (P_Desc_dado_Spam * P_Spam) / P_Desc
P_NoSpam_dado_Desc = (P_Desc_dado_NoSpam * P_NoSpam) / P_Desc

print("--- Clasificador Naive Bayes ---")
print(f"Probabilidad a Priori de Spam: {P_Spam:.2f}")
print(f"Probabilidad a Priori de No Spam: {P_NoSpam:.2f}")
print("-" * 30)

print(f"P('Descuento'): {P_Desc:.4f}")
print(f"P(Spam | 'Descuento'): {P_Spam_dado_Desc:.4f}")
print(f"P(No Spam | 'Descuento'): {P_NoSpam_dado_Desc:.4f}")

# El clasificador elige la clase con la probabilidad a posteriori más alta
if P_Spam_dado_Desc > P_NoSpam_dado_Desc:
    print(" Clasificación: ¡SPAM!")
else:
    print(" Clasificación: NO SPAM")