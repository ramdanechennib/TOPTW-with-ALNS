import math
from location import Location

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Extracting k, v, N, t
    k, v, N, t = map(int, lines[0].split())
    
    # Extracting D, Q
    D, Q = map(int, lines[1].split())
    
    # Extracting point data
    points = []
    for line in lines[2:]:
        data = list(map(float, line.split()))
        i, x, y, d, S, O, C = int(data[0]), data[1], data[2], data[3], data[4], int(data[-2]), int(data[-1])
        points.append(Location(i, x, y, d, S, O, C))
        
    return k, v, N, t, D, Q, points

def wait_time(t_arrive, t_open):
    return max(0, t_open - t_arrive)

def travel_time(loc1, loc2):
    return round(math.sqrt((loc1.x - loc2.x) ** 2 + (loc2.y - loc1.y) ** 2), 2)

def t_arrive(path, loc_index):
    if loc_index == 0:
        return 0
    else:
        last_city = path[loc_index - 1]
        current_city = path[loc_index]
        return last_city.departure_time + travel_time(last_city, current_city)
