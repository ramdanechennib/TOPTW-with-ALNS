import pygame
import pygame.freetype

from les_fun_interface import build_edges, read_solution, update, wait_time
from repair import calculate_profit, calcule_time_pathe

pygame.init()

# إعدادات الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (169, 169, 169)

# إعدادات الشاشة
SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 780
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('generate_sol')

# الخط
FONT = pygame.freetype.SysFont("Segoe Print", 18)
# متغيرات لشريط التمرير
scroll_y1 = 0
scroll_y2 = 0
scroll_y3 = 0
scroll_height = 100
scroll_pos1 = 0
scroll_pos2 = 0
scroll_pos3 = 0
scrolling1 = False
scrolling2 = False
scrolling3 = False
scroll_speed1 = 0
scroll_speed2 = 0
scroll_speed3 = 0
scroll_deceleration = 0.05

# الدوال لرسم العناصر
def draw_text(surface, text, pos, color=BLACK):
    FONT.render_to(surface, pos, text, color)

def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

def draw_button(surface, text, pos, size=(150, 40)):
    draw_rounded_rect(surface, GRAY, (*pos, *size), 15)
    draw_text(surface, text, (pos[0] + 10, pos[1] + 10))

def draw_table(surface, rect, rows, cols, headers, col_widths, data=None, scroll_y=0, max_height=None):
    x, y, width, height = rect
    cell_height = height // (rows + 1)

    for i in range(rows + 1):
        col_x = x
        for j in range(cols):
            cell_width = col_widths[j]
            cell_y = y + i * cell_height - scroll_y
            if y <= cell_y <= (y + height - cell_height) and (max_height is None or cell_y < max_height):
                pygame.draw.rect(surface, LIGHT_GRAY, (col_x, cell_y, cell_width, cell_height))
                pygame.draw.rect(surface, BLACK, (col_x, cell_y, cell_width, cell_height), 1)
                if i == 0:
                    draw_text(surface, headers[j], (col_x + 5, cell_y + 5))
                elif data and i - 1 < len(data):
                    if j < len(data[i - 1]):
                        draw_text(surface, data[i - 1][j], (col_x + 5, cell_y + 5))
                    else:
                        draw_text(surface, "", (col_x + 5, cell_y + 5))
                else:
                    draw_text(surface, "", (col_x + 5, cell_y + 5))
            col_x += cell_width

def handle_button_click(pos, button_rect,fun,solution,graph):
    if button_rect.collidepoint(pos):
        print("Start algorithm button clicked")
        draw_graph(fun,graph,solution)  # Replace with the appropriate function as needed
clock = pygame.time.Clock()

speed = 9
def dessin_best_sol(screen,graph,  best_solution):
    global  clock, speed
    paths = read_solution(best_solution)
    build_edges(paths)
    update(paths, graph, screen)

def dessine_sol_initial(screen,graph, initial_solution):
    global   clock, speed
    paths = read_solution(initial_solution)
    build_edges(paths)
    update(paths, graph, screen)

def draw_graph(draw_function,graph,solution):
    print("Graph drawing")
    background_image_path = r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\pikaso_texttoimage_An-old-worn-map-with-a-weathered-distressed-appear.jpeg'
    pygame.init()
    graph_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Graph Display')
    
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        graph_screen.blit(background_image, (0, 0))  # Display background image
        draw_function(graph_screen,graph,solution)  # Draw the graph based on the passed function
        pygame.display.flip()

    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('New Frame')

def handle_scrollbar_click(pos, scroll_rect, scroll_id):
    global scrolling1, scroll_pos1, scroll_speed1, scrolling2, scroll_pos2, scroll_speed2, scrolling3, scroll_pos3, scroll_speed3
    if scroll_rect.collidepoint(pos):
        if scroll_id == 1:
            scrolling1 = True
            scroll_pos1 = pos[1]
            scroll_speed1 = 0
        elif scroll_id == 2:
            scrolling2 = True
            scroll_pos2 = pos[1]
            scroll_speed2 = 0
        elif scroll_id == 3:
            scrolling3 = True
            scroll_pos3 = pos[1]
            scroll_speed3 = 0

def affiche_result(solution, travel_time, sol_id, profit,fun,graph):
    global scroll_y1, scroll_y2, scroll_y3, scroll_pos1, scroll_pos2, scroll_pos3, scroll_speed1, scroll_speed2, scroll_speed3, scrolling1, scrolling2, scrolling3
    scroll_y1 = 0
    scroll_y2 = 0
    scroll_y3 = 0
    scrolling1 = False
    scrolling2 = False
    scrolling3 = False

    path_data = []
    for idx, route in enumerate(sol_id):
        vehicle_id = f"V{idx+1}"
        route_info = f"{route}"
        current_route = solution[idx]
        route_profit = calculate_profit(current_route)
        route_time = calcule_time_pathe(current_route, current_route[0])
        path_data.append([vehicle_id, route_info, str(route_profit), str(route_time)])

    city_data = []
    for route in solution:
        for index, loc in enumerate(route):
            if index == 0:  # Check if it is the first location in the route
                arrive_time = 0
                departure_time = 0
                d = 0 
                wait = 0
            else:
                arrive_time = loc.arrival_time 
                departure_time = loc.departure_time 
                d = loc.d 
                wait = wait_time(loc.arrival_time, loc.O)
            city_data.append([
                f"City {loc.i}",
                str(loc.S),
                str(round(arrive_time)),
                str(round(wait)),
                str(round(d)),
                str(round(departure_time))
            ])
    city_time = []
    for i in range(0, len(travel_time), 3):
        city_time.append([str(travel_time[i]), str(travel_time[i+1]), str(round(travel_time[i+2]))])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if fun=="initial":

                          handle_button_click(event.pos, button_rect,dessine_sol_initial,solution,graph)
                    else:
                          handle_button_click(event.pos, button_rect,dessin_best_sol,solution,graph)
                    handle_scrollbar_click(event.pos, scroll_rect1, 1)
                    handle_scrollbar_click(event.pos, scroll_rect2, 2)
                    handle_scrollbar_click(event.pos, scroll_rect3, 3)
                elif event.button == 4:  # Scroll up
                    if scroll_rect1.collidepoint(event.pos):
                        scroll_y1 = max(0, scroll_y1 - 20)
                    elif scroll_rect2.collidepoint(event.pos):
                        scroll_y2 = max(0, scroll_y2 - 20)
                    elif scroll_rect3.collidepoint(event.pos):
                        scroll_y3 = max(0, scroll_y3 - 20)
                elif event.button == 5:  # Scroll down
                    if scroll_rect1.collidepoint(event.pos):
                        scroll_y1 = min(scroll_y1 + 20, 100)
                    elif scroll_rect2.collidepoint(event.pos):
                        scroll_y2 = min(scroll_y2 + 20, 350)
                    elif scroll_rect3.collidepoint(event.pos):
                        scroll_y3 = min(scroll_y3 + 20, 400)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    scrolling1 = False
                    scrolling2 = False
                    scrolling3 = False
            elif event.type == pygame.MOUSEMOTION:
                if scrolling1:
                    dy = event.pos[1] - scroll_pos1
                    scroll_speed1 = dy
                    scroll_pos1 = event.pos[1]
                elif scrolling2:
                    dy = event.pos[1] - scroll_pos2
                    scroll_speed2 = dy
                    scroll_pos2 = event.pos[1]
                elif scrolling3:
                    dy = event.pos[1] - scroll_pos3
                    scroll_speed3 = dy
                    scroll_pos3 = event.pos[1]

        if not scrolling1:
            scroll_speed1 *= scroll_deceleration
        if not scrolling2:
            scroll_speed2 *= scroll_deceleration
        if not scrolling3:
            scroll_speed3 *= scroll_deceleration

        scroll_y1 = max(0, min(scroll_y1 + scroll_speed1, 100))
        scroll_y2 = max(0, min(scroll_y2 + scroll_speed2, 350))
        scroll_y3 = max(0, min(scroll_y3 + scroll_speed3, 400))

        screen.fill(WHITE)
        if pygame.display.get_surface() is not None:
            screen.fill(WHITE)

            draw_text(screen, "affichage de detaille de path", (10, 10))
            draw_text(screen, "affichage de detaille de ville", (10, 200))
            draw_text(screen, "le profite total de solution", (1200, 580))
            draw_text(screen, "la forme de best  solution:", (600, 680))
            draw_text(screen, "le travel time ", (1250, 20))

            draw_table(screen, (170, 45, 900, 150), len(sol_id), 4, ["viecule", "route", "profit", "time de route"], [50, 500, 100, 150], path_data, scroll_y1, max_height=150)
            draw_table(screen, (170, 225, 900, 700), len(city_data), 6, ["ville", "profite de ville", "temp arriver", "waite time","service time", "deparute_time"], [150, 150, 150, 150, 150, 150], city_data, scroll_y2, max_height=610)
            draw_table(screen, (1220, 50, 200, 700), len(city_time), 3, ["City1", "City 2", "travel_time"], [70, 70, 115], city_time, scroll_y3, max_height=500)

            scroll_rect1.y = 50 + scroll_y1
            scroll_rect2.y = 225 + scroll_y2
            scroll_rect3.y = 50 + scroll_y3
            draw_rounded_rect(screen, DARK_GRAY, scroll_rect1, 7)
            pygame.draw.rect(screen, BLACK, scroll_rect1, 1, border_radius=7)
            draw_rounded_rect(screen, DARK_GRAY, scroll_rect2, 7)
            pygame.draw.rect(screen, BLACK, scroll_rect2, 1, border_radius=7)
            draw_rounded_rect(screen, DARK_GRAY, scroll_rect3, 7)
            pygame.draw.rect(screen, BLACK, scroll_rect3, 1, border_radius=7)
            
            draw_button(screen, "draw graphe", (10, 610))

            pygame.draw.rect(screen, LIGHT_GRAY, (10, 720, 1480, 30))
            pygame.draw.rect(screen, BLACK, (10, 720, 1480, 30), 1)
            draw_text(screen, f"Solution: {sol_id}", (10, 723))

            pygame.draw.rect(screen, LIGHT_GRAY, (1300, 610, 70, 30))
            pygame.draw.rect(screen, BLACK, (1300, 610, 70, 30), 1)
            draw_text(screen, str(profit), (1300, 613))

            pygame.display.flip()
        else:
            print("Display surface is no longer available.")
            running = False
    

# زر التفعيل
button_rect = pygame.Rect(10, 610, 150, 40)
scroll_rect1 = pygame.Rect(1100, 50, 20, 20)
scroll_rect2 = pygame.Rect(1100, 225, 20, 20)
scroll_rect3 = pygame.Rect(1490, 50, 20, 20)
scroll_deceleration = 0.05
scroll_pos1 = scroll_pos2 = scroll_pos3 = 0
scrolling1 = scrolling2 = scrolling3 = False
scroll_y1 = scroll_y2 = scroll_y3 = 0
