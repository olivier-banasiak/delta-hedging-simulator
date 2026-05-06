import numpy as np
from pricer import * # Importe bs_price et bs_delta
from simulation import simulate_gbm

def run_hedging_simulation(trajectoire_prix, K, T, r, sigma):
    # 1. Préparation des constantes
    n_steps = len(trajectoire_prix) - 1
    dt = T / n_steps #l'intervalle de temp 
    S0 = trajectoire_prix[0]
    
    # 2. Jour 0 : Mise en place de la couverture
    # On vend l'option (on reçoit du cash)
    prix_option_initial = bs_price(S0, K, T, r, sigma, option_type="call")
    # On calcule le delta initial
    delta_actuel = bs_delta(S0, K, T, r, sigma, option_type="call")
    
    # Portefeuille initial = Cash reçu - Achat des actions de couverture
    portefeuille_cash = prix_option_initial - (delta_actuel * S0)
    
    # 3. Boucle de rebalancement (du jour 1 au dernier jour)
    for i in range(1, n_steps + 1):
        St = trajectoire_prix[i]
        
        # A. On fait tourner les intérêts sur le cash emprunté/déposé (Le coût du temps)
        portefeuille_cash *= np.exp(r * dt)
        
        # B. Calcul du temps restant (important : tau tend vers 0)
        tau = max(T - (i * dt), 1e-9) # On évite division par zéro à l'échéance
        
        # C. Ajustement du Delta
        nouveau_delta = bs_delta(St, K, tau, r, sigma, option_type="call")
        variation_delta = nouveau_delta - delta_actuel
        
        # D. On achète/vend les actions et on met à jour le cash
        portefeuille_cash -= variation_delta * St
        
        # E. On mémorise le delta pour le lendemain
        delta_actuel = nouveau_delta
        
    # 4. Échéance (T)
    S_final = trajectoire_prix[-1]
    
    # Valeur de notre stratégie de couverture
    valeur_couverture_finale = (delta_actuel * S_final) + portefeuille_cash
    
    # Ce que l'on doit payer au client (Payoff du Call)
    payoff_client = max(S_final - K, 0)
    
    # PnL Final (doit être proche de 0 si le hedge est bon)
    pnl_final = valeur_couverture_finale - payoff_client
    
    return pnl_final


trajectoire = simulate_gbm(100, 1, 0.05, 0.2, 252)
pnl = run_hedging_simulation(trajectoire, 100, 1, 0.05, 0.2)
print(f"Résultat du hedging : {pnl:.2f} €")