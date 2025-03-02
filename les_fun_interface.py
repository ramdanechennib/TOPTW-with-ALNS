import math
import pygame
from alns import f
from generate_solution import create_solution
from location import Location
max_iterations = 1000
initial_temperature = 500
number_of_segments = 50
total_solution_profit = 12000
best_solution_form = "Form 1"
pygame.display.set_caption("Routes Visualization")
clock = pygame.time.Clock()
radius = 12
speed = 2  # This controls the frame rate, higher value means faster updates
grey = (100, 100, 100)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (200, 0, 0)
black = (0, 0, 0)
blue = (50, 50, 160)
# Colors for paths
path_colors = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255)    # Cyan
]
def edge_id(n1, n2):
    return tuple(sorted((n1, n2)))
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
def read_input_data(file_path):
    k, v, N, t, D, Q, points = read_data(file_path)
    depot = points[0]  # Assuming the first point is the depot
    Tmax = depot.C  # تحديد Tmax بناءً على وقت إغلاق المستودع
    return k, v, N, t, D, Q, points, depot, Tmax
def generate_solution(file_path='c101.txt', solution_method="inser_fin",number_of_paths=3):
    global best_solution, initial_solution, unvisited_points_global
    k, v, N, t, d, Q, points, depot, Tmax = read_input_data(file_path)
    
    solutions = []

    solution, unvisited_points = create_solution(points, number_of_paths, depot, Tmax, method=solution_method)
    initial_solution = solution
    unvisited_points_global = unvisited_points
    profite_tot = f(solution)
    print("le profite de la solution initiale est ", profite_tot)

    return initial_solution, unvisited_points,solution_method,points,depot, Tmax
def display_initial_solution(solution_method, solutions, unvisited_points):
    solution_finale = [[loc.i for loc in route] for route in solutions]
    print(f"La solution initiale avec la methode {solution_method} : {solution_finale}")
    uninserted = [loc.i for loc in unvisited_points]  # La liste L
    print(f"La liste de points non insérés après la solution initiale est : {uninserted}")
    for route in solution_finale:
        
        print(f"L'indice de la route est : {route}")
        for rout in route :
            print(f"L'indice de la route est : {rout}")
    return solution_finale,solutions
# Pygame visualization functions
def edge_id(n1, n2):
    return tuple(sorted((n1, n2)))
def build_edges(paths):
    global edges
    edges = {}
    for path_idx, path in enumerate(paths):
        color = path_colors[path_idx % len(path_colors)]
        for i in range(len(path) - 1):
            n1, n2 = path[i], path[i + 1]
            eid = edge_id(n1, n2)
            if eid not in edges:
                edges[eid] = [(n1, n2), color]
def draw_text(text, position, screen,color):
    font = pygame.font.Font(None, 22)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (position[0] - text_surface.get_width() // 2, position[1] - text_surface.get_height() // 2))
def circle_fill(xy, line_color, fill_color, radius, thickness, screen):
    pygame.draw.circle(screen, line_color, xy, radius)
    pygame.draw.circle(screen, fill_color, xy, radius - thickness)
def display_city_image(xy, screen, city_image_path, radius):
    # تحميل صورة المدينة وضبط حجمها لتناسب الدائرة
    city_image = pygame.image.load(city_image_path).convert_alpha()
    city_image = pygame.transform.scale(city_image, (2.5 * radius, 2.5 * radius))
    
    # الحصول على الإحداثيات لتمركز الصورة
    image_rect = city_image.get_rect(center=xy)
    
    # عرض صورة المدينة على الشاشة
    screen.blit(city_image, image_rect)
def update(paths, graph, screen):
    global clock
    draw_graph(paths, graph, screen)
    pygame.display.update()
    clock.tick(speed)
city_image_path= r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\gps_13796392.png'
background_image_pat =r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\pikaso_texttoimage_An-old-worn-map-with-a-weathered-distressed-appear.jpeg'
def draw_graph(paths, graph, screen):
    global edges, city_image_path

    # تحميل صورة الخلفية وضبط حجمها لتناسب الشاشة
    background_image = pygame.image.load(background_image_pat).convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())

    # عرض صورة الخلفية
    screen.blit(background_image, (0, 0))
    
    # باقي الكود لرسم النقاط والمسارات
    for i, (xy, _, _, _) in enumerate(graph):
        display_city_image(xy, screen, city_image_path, radius)
        draw_text(str(i), xy, screen, white)

    for e in edges.values():
        (n1, n2), color = e
        if n1 >= len(graph) or n2 >= len(graph):
            print(f"Invalid edge indices: {n1}, {n2}")
            continue
        pygame.draw.line(screen, color, graph[n1][0], graph[n2][0], 3)

    for path_idx, path in enumerate(paths):
        color = path_colors[path_idx % len(path_colors)]
        for i in path:
            xy = graph[i][0]
            display_city_image(xy, screen, city_image_path, radius)
            
            draw_text(str(i), xy, screen, color)
car_image_paths = [
    r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\ambulance_15792564.png',
    r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\3d-car_10740612.png',
    # أضف مسارات أخرى لصور السيارات هنا
]
  # بدء مواقع السيارات على المسارات
pygame.init()
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Graph Display')
def scale_coordinates(points, display_width, display_height):
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    
    # Calculate scale factors
    scale_x = display_width / (max_x - min_x)
    scale_y = display_height / (max_y - min_y)
    
    # Choose the smaller scale factor to maintain aspect ratio
    scale = min(scale_x, scale_y) * 0.96  # Slightly reduce to avoid points being too close to the edges
    
    # Offset to center the graph
    offset_x = (display_width - (max_x - min_x) * scale) / 2
    offset_y = (display_height - (max_y - min_y) * scale) / 2
    
    for point in points:
        point.x = (point.x - min_x) * scale + offset_x
        point.y = (point.y - min_y) * scale + offset_y
def create_graph(points):
    graph = []
    for point in points:
        coords = (int(point.x), int(point.y))
        adjacents = []
        graph.append([coords, adjacents, grey, black])
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            distance = math.sqrt((points[i].x - points[j].x)**2 + (points[j].y - points[i].y)**2)
            if distance < 100:  # Adjust the threshold as needed
                graph[i][1].append(j)
                graph[j][1].append(i)
    
    return graph
def read_solution(solution):
    paths = []
    for path in solution:
        paths.append([loc.i for loc in path])
    return paths
def dessin_best_sol(graph):
    global  best_solution, screen, clock, speed
    paths = read_solution(best_solution)
    build_edges(paths)
    update(paths,graph)
def dessin_toutes_best_solutions(graph):
    global  file_de_solution, screen, clock, speed
    for i, best_solution in enumerate(file_de_solution):
        paths = read_solution(best_solution)
        build_edges(paths)
        update(paths,graph)
        pygame.time.wait(200)  # Wait for 1 second between each solution for better visualization
