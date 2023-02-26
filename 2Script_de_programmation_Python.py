import numpy as np #  pour les opérations mathématiques
import matplotlib.pyplot as plt # pour tracer les graphiques
import random
from scipy.integrate import odeint # pour résoudre les problèmes de valeurs initiales des EDO dans le MSIRD

# MODÈLE STOCHASTIQUE
# définir les conditions initiales
# lorsque le nombre de personnes dans ces groupes change, de nouvelles valeurs seront ajoutées aux listes
S = [1197] 
I = [3]
R = [0]
t = [0]

# fin du temps, quand arrêter la simulation
tend = 1000

# définir les paramètres
beta = 40 * 0.001
gamma = 0.01


# boucle de la simulation de l'algorithme de Gillespie
while t[-1] < tend and (S[-1] + I[-1] >= 1):
  
    N = S[-1] + I[-1] + R[-1]

     # liste des propensions des événements à se produire 
    props = [beta*I[-1]*S[-1]/N, r*I[-1]]

    # calculer la somme des probabilités
    prop_sum = sum(props)

    # définir l'intervalle entre le moment présent et le moment de l'événement suivant
    # qui sera tiré d'une distribution aléatoire dépendant de la somme des propensions que cet événement se produit.
    tau = np.random.exponential(scale=1/prop_sum)
    t.append(t[-1]+tau)

    # tirage aléatoire entre 0 et 1 pour déterminer quel évènement va se passer
    rand = random.uniform(0,1)

    # une nouvelle infection : Susceptible devient Infecté
    if rand * prop_sum <= props[0]:
            S.append(S[-1] - 1)
            I.append(I[-1] + 1)
            R.append(R[-1])
    
    # si ce n'est pas le cas du premier événement,  alors le deuxième événement doit se produire
    # un retrait : Infecté devient Récupéré
    else:
            S.append(S[-1])
            I.append(I[-1] - 1)
            R.append(R[-1] + 1)    

            

# tracer un graphique pour chaque variable du modèle
f,(ax1,ax2,ax3) = plt.subplots(3)

line1, = ax1.plot(t,S) # S
line2, = ax2.plot(t,I) # I
line3, = ax3.plot(t,R) # R



ax1.set_ylabel("S")
ax2.set_ylabel("I")
ax3.set_ylabel("R")
ax3.set_xlabel("Temps")


# MODÈLE DÉTERMINISTE
# fixer le point limite de t
t = np.linspace(0,tend, num=1000)


params = [beta,gamma]

# conditions initiales
y0 = [1197, 3, 0]


# créer une fonction 
def sim(variables, t, params):

    S = variables[0]
    I = variables[1]
    R = variables[2]

    N = S + I + R

    beta = params[0]
    gamma = params[1]

    # faire appel aux dérivées de chaque variable
    dSdt = -beta * I * S / N
    dIdt = beta * I * S / N - r * I
    dRdt = gamma * I

    return([dSdt, dIdt, dRdt])

# résoudre un système des EDO
y = odeint(sim, y0, t, args=(params,))


line1, = ax1.plot(t,y[:,0]) # S
line2, = ax2.plot(t,y[:,1]) # I
line3, = ax3.plot(t,y[:,2]) # R

# montrer les graphiques des résultats déterministes (orange) et stochastiques (bleu)
plt.show()
