"""

J'ai la simulation du prix de l'action via un mouvement brownien. 
Pour la formule du rendement : l'action va croitre avec le taux sans riqeu auquel on eleve la volaitilité lié au 
lemem d'ito, auquel on ajoute le mouvmeent brownien multiplié par la racine carré du temp c'est liée a la variance et 
l'ecart type


"""
import numpy as np
import matplotlib.pyplot as plt # La librairie magique pour dessiner des graphiques

def simulate_gbm(S0, T, r, sigma, steps=252):
    """
    Simule une trajectoire d'action via un Mouvement Brownien Géométrique.
    steps = 252 (le nombre de jours de bourse dans une année)
    """
    # On découpe le temps T en petits morceaux (1 jour)
    dt = T / steps
    
    # On initialise notre liste avec le prix de départ
    prix = [S0]
    S_actuel = S0
    
    # On fait une boucle 'for' (plus sûr que 'while' pour éviter les boucles infinies)
    for _ in range(steps):
        # 1. On tire notre choc de marché sur la loi normale
        Z = np.random.normal(0, 1) # génére un nombre réel aléatoire
        
        # 2. La vraie formule d'un rendement boursier (pourcentage)
        rendement = np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        
        # 3. On met à jour le prix en le multipliant par ce rendement
        S_actuel = S_actuel * rendement
        
        # 4. On stocke le nouveau prix dans la liste
        prix.append(S_actuel)
        
    return prix

# --- PARAMÈTRES DU MARCHÉ ---
S0 = 100      # Prix initial
T = 1.0       # 1 an
r = 0.05      # Taux sans risque (5%)
sigma = 0.20  # Volatilité (20%)

# --- EXÉCUTION ---
trajectoire = simulate_gbm(S0, T, r, sigma)

# --- AFFICHAGE GRAPHIQUE ---
plt.figure(figsize=(10, 6))
plt.plot(trajectoire, color='blue', linewidth=1.5)
plt.title("Simulation du prix de l'action (Mouvement Brownien)")
plt.xlabel("Jours de trading")
plt.ylabel("Prix de l'action (€)")
plt.axhline(y=S0, color='red', linestyle='--', label="Prix initial")
plt.grid(True)
plt.legend()
plt.show()