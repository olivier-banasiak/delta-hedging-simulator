"""
Ici c'est le mathématicien qui va calculer en fonction des données le prix de l'action 
et le delta.
Rappel : 
- d1 : distance entre le spot et le strike 
- d2 : d1 auquel on a enlevé l'incertitude du marché via la volatilité donc on peut plus gagner enormement d'argent 
- N(d1) : pourcentage d'etre dans la monnaie en prenant en compte la volatilité 

Pour la formule du call : profit esperé - ce que je paye : 
    - pour le profit espere a l'echeance on obtient S ssi on exerce l'option avec probas N(d1) 
    - pour ce que je paye : si l'option est levée avec probas N(d2) alors je paye le strike que j'actualise a aujourd'hui 

Pour la formule du put : ce que j'espere recevoir a l'echeance - ce que je devrais payer 
    - pour ce que j'espere recevoir si le put est confirmé c'est le strike actualisé avec probas N(-d2)
    - ce que je paye c'est le spot a l'instant T avec probas N(-d1) 
"""

import numpy as np
from scipy.stats import norm

def d1_d2(S, K, T, r, sigma):
    """Calcule les paramètres d1 et d2 de Black-Scholes."""
    # Sécurité : éviter la division par zéro si on est à l'échéance
    if T <= 0.0 or sigma <= 0.0:
        return 0.0, 0.0
    
    # --- TODO 1 : Calcule d1 ---
    # Correction : np.log au lieu de np.ln, et ajout des parenthèses au dénominateur
    d1 = (np.log(S / K) + (r + (sigma**2) / 2) * T) / (sigma * np.sqrt(T))
    
    # --- TODO 2 : Calcule d2 ---
    # Correction : utilisation de np.sqrt() pour la propreté (équivalent à T**0.5)
    d2 = d1 - sigma * np.sqrt(T)
    
    return d1, d2

def bs_price(S, K, T, r, sigma, option_type="call"):
    """Calcule le prix d'une option (Call ou Put)."""
    # Gestion de la date d'échéance (Le Payoff exact)
    if T <= 0.0:
        if option_type == "call":
            return max(S - K, 0.0)
        elif option_type == "put":
            return max(K - S, 0.0)
    
    d1, d2 = d1_d2(S, K, T, r, sigma)
    
    if option_type == "call":
        # --- TODO 3 : Prix du Call ---
        # Correction : ajout de .cdf() après norm
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) 
        
    elif option_type == "put":
        # --- TODO 4 : Prix du Put ---
        # Correction : ajout de .cdf() après norm
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1) 
    else:
        raise ValueError("Erreur: option_type doit être 'call' ou 'put'")

def bs_delta(S, K, T, r, sigma, option_type="call"):
    """Calcule le Delta d'une option (Call ou Put)."""
    # Gestion de la date d'échéance (La certitude absolue)
    if T <= 0.0:
        if option_type == "call":
            return 1.0 if S > K else 0.0
        elif option_type == "put":
            return -1.0 if S < K else 0.0
            
    d1, d2 = d1_d2(S, K, T, r, sigma)
    
    if option_type == "call":
        # --- TODO 5 : Delta du Call ---
        # Correction : ajout de .cdf()
        return norm.cdf(d1)
        
    elif option_type == "put":
        # --- TODO 6 : Delta du Put ---
        # Correction : ajout de .cdf() (ta logique mathématique norm(d1) - 1 était parfaite !)
        return norm.cdf(d1) - 1 
    else:
        raise ValueError("Erreur: option_type doit être 'call' ou 'put'")