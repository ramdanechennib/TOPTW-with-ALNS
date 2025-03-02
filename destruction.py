import copy
import random

from read_data import t_arrive, travel_time, wait_time
from repair import calculate_profit
def time_based_removal(solution, num_remove):
    time_delays = []
    print("time_based_removal")

    for path in solution:
        for i in range(len(path) - 1):
            city = path[i]
            next_city = path[i + 1]
            travel_tim = travel_time(city, next_city)
            arrival_time = t_arrive(path, i)
            wait = wait_time(arrival_time, city.O)
            departure_time = arrival_time + wait + city.d
            delay = departure_time - arrival_time
            
            city.arrival_time = arrival_time
            city.departure_time = departure_time
            city.delay = delay
            
            time_delays.append((city, delay))
    time_delays.sort(key=lambda x: -x[1])
    removed_cities = [city for city, delay in time_delays[:num_remove]]
    for city in removed_cities:
        for path in solution:
            if city in path:
                path.remove(city)
    
    update_city_times(solution)
    
    return solution, removed_cities


def random_removal(solution, q):
    print("random_removal")
    solution_finale = [[loc.i for loc in route] for route in solution] 
    print("la solution qui choisie pour la suppression   ",solution_finale)
    solutions = copy.deepcopy(solution)
    all_tasks = [task for route in solutions for task in route if task.i != route[0].i]
    
    removed_tasks = []
    while q > 0 and all_tasks:
        y = random.randint(0, len(all_tasks) - 1)
        r = all_tasks[y]
        all_tasks.pop(y)
        removed_tasks.append(r)
        q -= 1
    
    # Mettre à jour les routes en supprimant les tâches enlevées
    for route in solutions:
        for task in removed_tasks:
            if task in route:
                route.remove(task)
    update_city_times(solutions)
    
    return solutions, removed_tasks

def Worst_removal_randome_y(solution, q):
    print ("Worst_removal_randome_y")
    # solution_finale = [[loc.i for loc in route] for route in solution] 
    # print("la solution qui choisie pour la suppression   ",solution_finale)
    p = 3.14
    solutions = copy.deepcopy(solution)
    all_ville = [ville for route in solutions for ville in route if ville.i != route[0].i]
    
    # Trier toutes les villes par l'attribut S
    all_ville = sorted(all_ville, key=lambda loc: loc.S)
    
    all_tasks = copy.deepcopy(all_ville)
    
    # Points triés pour le débogage
    # points_sorted = [loc.i for loc in all_tasks]
    # print("points_sorted_de la solution dans la suppression ", points_sorted)
    
    removed_tasks = []
    
    while q > 0 and all_tasks:
        y = random.random()
        index = int(y ** p * len(all_tasks))
        r = all_tasks[index]
        
        for route in solutions:
            for rout in route:
                if rout.i==r.i:
                    route.remove(rout)
                    break
        
        all_tasks.remove(r)
        removed_tasks.append(r)
        q -= 1
    update_city_times(solutions)
    
    return solutions, removed_tasks
def Worst_removal(solution, q ):

    print ("Worst_removal")
    solution_finale = [[loc.i for loc in route] for route in solution] 
    # print("la solution qui choisie pour la suppression   ",solution_finale)
    solutions = copy.deepcopy(solution)
    all_task = [task for route in solutions for task in route if task.i != route[0].i]
    all_task = sorted(all_task, key=lambda loc: loc.S, reverse=False)
    all_tasks = copy.deepcopy(all_task)
    # all = [loc.i for loc in all_tasks]
    # print("sorted", all)   
    
    removed_tasks = []
    for _ in range(q):
        removed_element = all_tasks[0]
        # print(f"hhhhhh{removed_element.i}")
        all_tasks.pop(0)
        # print([loc.i for loc in all_tasks])
        removed = False
        for element in solution:
            for e in element:
                if removed_element.i == e.i:
                    removed = True
                    removed_tasks.append(e)
                    element.remove(e)
                    break
            if removed:
                break
    all = [loc.i for loc in removed_tasks]
    all2 = [[loc.i for loc in route] for route in solution]
    print("removed_tasks", all)   
    # print(f" la solution appre suprimer{all}est{all2}  ")  
    update_city_times(solution)
     
    return solution, removed_tasks

def update_solution(solutions,method,q,p):
    solution = copy.deepcopy(solutions)
    if method == "Worst_removal":
            removed_tasks, all_tasks = Worst_removal_randome_y(solution, q)
    elif method == "random_removal":
            removed_tasks, all_tasks = random_removal(solution, q)
    removed = [loc.i for loc in removed_tasks]
    all = [loc.i for loc in all_tasks]
    # print(f"les villes qui sepprimer est :\n {removed}")

    # print(f"la liste des ville Cela restait:\n {all}")    
    for rout in solution:
        for ville in rout:
            for tasks in removed_tasks:
                if tasks.i == ville.i:
                    rout.remove(ville)


    return solution,removed_tasks

def update_solution_score(solution):
    total_score = 0
    for path in solution:
        total_score += calculate_profit(path)
    return total_score
def update_city_times(solution):
    for path in solution:
        for i in range(len(path)):
            city = path[i]
            if i == 0:
                city.arrival_time = 0
                city.departure_time = city.arrival_time + city.d
            else:
                arrival_time = t_arrive(path, i)
                
                city.arrival_time = arrival_time
                wait = wait_time(city.arrival_time, city.O)
                city.departure_time = city.arrival_time + wait + city.d
                city.delay = city.departure_time - city.arrival_time
