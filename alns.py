import copy
import math
import random

from destruction import Worst_removal, Worst_removal_randome_y, random_removal, update_solution
from generate_solution import create_solution

from repair import repaire_greedy

def acceptance_criteria(S_prime, S, T, f):
    if f(S_prime) <=f(S):  # Remarque : nous maximisons le profit
        delta_f = f(S_prime) - f(S)
        acceptance_probability = math.exp(delta_f / T)
        return random.random() < acceptance_probability

def update_temperature(T, phi=0.99975):
    return T * phi
import random
import os
def ALNSv1(S_init, D, R, liste_non_visited,  max_iteration, segment, depot, Tmax):
    # Initialisation
   
    seg_1 = 33
    seg_2 = 9
    seg_3 = 13
    rho_react = 0.1  # Ajuster selon les besoins
    S_best = copy.deepcopy(S_init) 
    S = copy.deepcopy(S_init) 
    omega_T = 0.05
    fc_S = f(S)
    T = - (omega_T * fc_S) / math.log(0.5)  # Initialiser T (Température initiale)
    
    nbr_iteration = 0
    # Initialiser les scores, poids et probabilité pour les opérateurs D
    scores_D = {d: 0 for d in D}
    weights_D = {d: 1 for d in D}
    probabilities_D = {d: 1/len(D) for d in D}
    nd_D = {d: 0 for d in D}  # Nombre d'utilisation de chaque opérateur de destruction
    
    # Initialiser les scores, poids et probabilité pour les opérateurs R
    scores_R = {r: 0 for r in R}
    weights_R = {r: 1 for r in R}
    probabilities_R = {r: 1/len(R) for r in R}
    nd_R = {r: 0 for r in R}  # Nombre d'utilisation de chaque opérateur de réparation
    file_de_solution=[]
    while nbr_iteration <= max_iteration:
        print ("------------------------------------------------------------------------")    
        print("iteration",nbr_iteration)
        S_prime = copy.deepcopy(S)
        liste_r=copy.deepcopy(liste_non_visited)
        # Tirer un nombre aléatoire
        q = random.randint(1, len(S_prime))
        
        # Choisir un opérateur de destruction d ∈ D par la roulette
        d = random.choices(list(D), weights=probabilities_D.values(), k=1)[0]
        
        # Appliquer l'opérateur de destruction
        
        S_prim, removed_tasks = d(S_prime, q)
       # print(removed_tasks)
        # print("gggggggggggggggggggggggggggggggf",S_prime)
        # Ajouter les tâches à externaliser
        
        liste_r.extend(removed_tasks)
        Uninserted = [loc.i for loc in liste_r] 
        print("la liste non visited in destriction",Uninserted)
        existe_dex(liste_r)
        if existe_dex(liste_r):
            break
        # Incrémenter le nombre d'utilisation de l'opérateur de destruction
        nd_D[d] += 1
        # Choisir un opérateur de réparation r ∈ R par la roulette
        r = random.choices(list(R), weights=probabilities_R.values(), k=1)[0]
        
        # Appliquer l'opérateur de réparation
        S_prim, liste_r = r(S_prim, liste_r, depot, Tmax)
        Uninserted = [loc.i for loc in liste_r] 
        print("la liste non visited in reparation",Uninserted)
        # for pat in S_prime:
        #     for gf in pat:
        #         for ds in liste_non_visited:
        #             if gf.i == ds.i:
        #                 liste_non_visited.remove(ds)
        # Uninserted = [loc.i for loc in liste_non_visited] 
        # print("la liste non visited in reparationtttttttttttttttttttt",Uninserted)
        existe_dex(liste_r)
        if existe_dex(liste_r):
            break
        # Incrémenter le nombre d'utilisation de l'opérateur de réparation
        nd_R[r] += 1
        

        if f(S_prim) > f(S_best):
            S_best = copy.deepcopy(S_prim)
            S = copy.deepcopy(S_prim)
            liste_non_visited=copy.deepcopy(liste_r)
            # Mettre à jour le score des opérateurs d et r
            scores_D[d] += seg_1
            scores_R[r] += seg_1
        elif f(S_prim) > f(S):
            S = copy.deepcopy(S_prim)
            liste_non_visited=copy.deepcopy(liste_r)
            # Mettre à jour le score des opérateurs d et r
            scores_D[d] += seg_2
            scores_R[r] += seg_2
        elif acceptance_criteria(S_prim, S, T, f):
            
            # Mettre à jour le score des opérateurs d et r
            scores_D[d] += seg_3
            scores_R[r] += seg_3
        
        T=update_temperature(T, phi=0.99975)
        file_de_solution.append(S_best)
        # print("file_de_solution",file_de_solution)
        nbr_iteration += 1
        solution_finale = [[loc.i for loc in route] for route in S_best]
        print(f" best solution de iteration {nbr_iteration}est {solution_finale} ")
        if nbr_iteration % segment == 0:
            # Mettre à jour les poids et probabilité des deux opérateurs d et r
            weights_D, probabilities_D = update_weights_and_probabilities(scores_D, weights_D, nd_D, rho_react)
            weights_R, probabilities_R = update_weights_and_probabilities(scores_R, weights_R, nd_R, rho_react)
            
            # Réinitialiser les scores des deux opérateurs d et r
            scores_D = {d: 0 for d in D}
            scores_R = {r: 0 for r in R}
        
        
        
        
    
    return S_best,file_de_solution

def f(solution):
    total_profit = 0
    for route in solution:
        for task in route:
            total_profit += task.S
    return total_profit
def update_weights_and_probabilities(scores, weights, nd, rho_react):
    updated_weights = {}
    for d in scores:
        theta_d = max(1, nd[d])
        updated_weights[d] = (1 - rho_react) * weights[d] + rho_react * (scores[d] / theta_d)
    total_weight = sum(updated_weights.values())
    updated_probabilities = {d: updated_weights[d] / total_weight for d in updated_weights}
    return updated_weights, updated_probabilities
def existe_dex(liste):
    """
    تحقق مما إذا كان هناك عنصر موجود مرتين أو أكثر في القائمة.
    
    Args:
    liste (list): قائمة العناصر.
    
    Returns:
    bool: True إذا كان هناك عنصر موجود مرتين أو أكثر، False إذا لم يكن هناك أي عنصر مكرر.
    """
    for i in range(len(liste) - 1):  # استخدام range بدلاً من len مباشرةً
        for j in range(i + 1, len(liste)):  # استخدام حلقة for للتحقق من العناصر بعد العنصر الحالي
            if liste[i].i == liste[j].i:  # مقارنة العناصر بناءً على خاصية .i
                print("laliste ay m3awda",liste[i].i)
                return True
    print("laliste ay non mm3awdach")
    return False

