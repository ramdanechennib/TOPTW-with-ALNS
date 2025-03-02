import copy
from repair import repaire_greedy, repaire_fin, shortest_path_insertion

def create_solution(liste_ville, nmber_path, depot, Tmax, method="greedy"):
    liste_non_visited = copy.deepcopy(liste_ville)
    for element in liste_non_visited:
          if element.i == depot.i:
                liste_non_visited.remove(element)
    paths = [[] for _ in range(nmber_path)]
    total_profit = 0
    if method == "greedy":
            paths, uninserted_points = repaire_greedy(paths,liste_non_visited, depot, Tmax )
    elif method == "inser_fin":
        for path in paths:
                path, uninserted_points = repaire_fin(liste_non_visited, depot, Tmax, path)
                
        liste_non_visited = uninserted_points
    elif method=="inser_time":
          paths, liste_non_visited=shortest_path_insertion(paths, liste_non_visited, depot, Tmax)
    
    #print(f"Total profits solution initial: {path_profit }")
    
    return paths, liste_non_visited