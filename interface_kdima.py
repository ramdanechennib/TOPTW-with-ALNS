import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog
from destruction import Worst_removal, Worst_removal_randome_y, random_removal, time_based_removal
from location import Location
import subprocess
from alns import ALNSv1, f
from les_fun_interface import build_edges, create_graph, display_initial_solution, generate_solution, read_input_data, read_solution, scale_coordinates, update, wait_time
from generate_solution import create_solution
from repair import calculate_profit, calcule_time_pathe, repaire_fin, repaire_greedy, shortest_path_insertion
import copy

# Initialize Pygame
pygame.init()
# Set the dimensions of the window
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('New Frame')
file_path = None
# Load background image
background_image = pygame.image.load('photo/artistic-blurry-colorful-wallpaper-background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Load return button image
return_button_image = pygame.image.load('photo/back (1).png')
return_button_image = pygame.transform.scale(return_button_image, (50, 50))
import_button_image = pygame.image.load('photo/txt-file-format.png')
import_button_image = pygame.transform.scale(import_button_image, (50, 50))
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200, 128)
LIGHT_GREY = (180, 180, 180)
BLUE = (0, 0, 255)
NAVY_BLUE = (0, 0, 128)
BLUE_NUIT = (0, 0, 50)
TEXT_COLOR = WHITE
clock = pygame.time.Clock()
radius = 12
speed = 9
# Define fonts
font = pygame.freetype.SysFont('segoe print', 24)
small_font = pygame.freetype.SysFont('segoe print', 16)
font = pygame.font.SysFont('segoe print', 16)  # Use Helvetica font, or Arial as a fallback
max_iteration=None
initial_temperature=None
segment=None
initial_solution = None
unvisited_points = None
depot=None
Tmax = None
graph = None
# Define text rendering function
# Define text rendering function
def render_text(text, font, color, surface, x, y, background=None):
    text = str(text)  # Ensure the text is a string
    if background is not None:
        textobj = font.render(text, True, color, background)
    else:
        textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# Define a function to draw rounded rectangles
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
# Define button class
class Button:
    def __init__(self, text, x, y, width, height, font, callback, args=None, image=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.font = font
        self.callback = callback
        self.args = args if args else []
        self.corner_radius = 15
        self.image = image

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            draw_rounded_rect(surface, self.color, self.rect, self.corner_radius)
            text_surface = self.font.render(self.text, True, BLUE_NUIT)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(text_surface, text_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback(*self.args)
# Define label class
class Label:
    def __init__(self, text, x, y, font):
        self.text = text
        self.font = font
        self.x = x
        self.y = y

    def draw(self, surface):
        render_text(self.text, self.font, WHITE, surface, self.x, self.y)
# Define checkbox class
class CheckBox:
    def __init__(self, text, x, y, font, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = WHITE
        self.font = font
        self.checked = False
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.checked:
            pygame.draw.line(surface, BLUE_NUIT, (self.rect.x, self.rect.y), (self.rect.x + 20, self.rect.y + 20), 2)
            pygame.draw.line(surface, BLUE_NUIT, (self.rect.x, self.rect.y + 20), (self.rect.x + 20, self.rect.y), 2)
        render_text(self.text, self.font, TEXT_COLOR, surface, self.rect.x + 25, self.rect.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                self.callback(self.checked)
# Define radiobutton class
class RadioButton:
    def __init__(self, text, x, y, font, group, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = WHITE
        self.font = font
        self.selected = False
        self.group = group
        self.callback = callback
        group.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.x + 10, self.rect.y + 10), 10)
        if self.selected:
            pygame.draw.circle(surface, BLUE_NUIT, (self.rect.x + 10, self.rect.y + 10), 5)
        render_text(self.text, self.font, TEXT_COLOR, surface, self.rect.x + 25, self.rect.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                for radio in self.group:
                    radio.selected = False
                self.selected = True
                self.callback(self.selected)
# Define table class
#    Table(['ville', 'profite de ville', 'temp arriver', 'waite time','departure'], [['', '', '', '','']], 600, 420, 700, 120, font)
class Table:
    def __init__(self, headers, rows, x, y, widths, height, font):
        self.headers = headers
        self.rows = rows
        self.rect = pygame.Rect(x, y, sum(widths), height)
        self.widths = widths  # قائمة عرض الأعمدة
        self.font = font

    def draw(self, surface):
        cell_height = 30
        x_offset = self.rect.x

        # رسم العناوين
        for i, header in enumerate(self.headers):
            render_text(header, self.font, TEXT_COLOR, surface, x_offset, self.rect.y)
            x_offset += self.widths[i] if i < len(self.widths) else 0

        # رسم الصفوف
        y_offset = self.rect.y + cell_height
        for row in self.rows:
            x_offset = self.rect.x
            for i, cell in enumerate(row):
                render_text(cell, self.font, TEXT_COLOR, surface, x_offset, y_offset)
                x_offset += self.widths[i] if i < len(self.widths) else 0
            y_offset += cell_height
def gener_sol(solution_method, initial_solution, unvisited_points):
    solution_finale, solutions = display_initial_solution(solution_method, initial_solution, unvisited_points)
    # تأكد من أن الجدول يحتوي على العدد الكافي من الصفوف
    while len(tables[0].rows) < len(solution_finale):
        tables[0].rows.append(['', '', '', ''])
    
    for i in range(len(solution_finale)):
        tables[0].rows[i][0] = i  # تحديث العمود 'vecule'
        tables[0].rows[i][1] = solution_finale[i]  # تحديث العمود 'route'
        
        # تحديث الجدول الثاني بالمدن
        # while len(tables[1].rows) < len(solution_finale[i]):
        #     tables[1].rows.append(['', '', '', '', ''])
        # for k in solution_finale[i]:
        #     tables[1].rows[k][0] = k

    for i in range(len(solutions)):
        tables[0].rows[i][2] = calculate_profit(solutions[i])  # تحديث العمود 'profit'
        tables[0].rows[i][3] = calcule_time_pathe(solutions[i], solutions[i][0])  # تحديث العمود 'time de route'

        # تحديث الجدول الثاني بالتفاصيل
        while len(tables[1].rows) < len(solutions[i]):
            tables[1].rows.append(['', '', '', '', ''])
        for k in range(len(solutions[i])):
            tables[1].rows[k][0] = solutions[i][k].i
            tables[1].rows[k][1] = solutions[i][k].S
            tables[1].rows[k][2] = solutions[i][k].arrival_time
            tables[1].rows[k][3] = wait_time(solutions[i][k].arrival_time, solutions[i][k].O)
            tables[1].rows[k][4] = solutions[i][k].departure_time

    profit = f(solutions)
    input_fields[2]['text'] = str(solution_finale)  # تحديث الحقل الثالث في قائمة input_fields
    input_fields[1]['text'] = str(profit)  # تحديث الحقل الثاني في قائمة input_fields
def dessine_sol_initial(screen):
    global graph, initial_solution, clock, speed
    paths = read_solution(initial_solution)
    build_edges(paths)
    update(paths, graph, screen)
def display_graph(SCREEN_WIDTH, SCREEN_HEIGHT, draw_function):
    background_image_ath= r'C:\Users\ramdan chennib\Desktop\projet\alns\photo\pikaso_texttoimage_An-old-worn-map-with-a-weathered-distressed-appear.jpeg'
    pygame.init()
    graph_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Graph Display')
    
    # تحميل صورة الخلفية وضبط حجمها لتناسب الشاشة
    background_image = pygame.image.load(background_image_ath).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        graph_screen.blit(background_image, (0, 0))  # عرض صورة الخلفية
        draw_function(graph_screen)  # رسم الحل الأولي أو الأفضل
        pygame.display.flip()

    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('New Frame')
# مثال لاستخدام الدالة
# display_graph(800, 600, dessine_sol_initial)  # لعرض الحل الأولي
# display_graph(800, 600, dessin_best_sol)  # لعرض الحل الأفضل
def generate_initial_solution():
    global value,initial_solution,profit_initial, unvisited_points, solution_method,depot, Tmax, points, file_path,graph,box
    if file_path is None:
        print("No file selected. Please import a data file first.")
        return
    number_of_paths = get_natural_number_from_input()
    
    if number_of_paths is None:
        print("Please enter a valid natural number for the number of paths.")
        return
    
    initial_solution, unvisited_points, solution_method, points,depot, Tmax = generate_solution(file_path, box,number_of_paths)
 
    new_points = copy.deepcopy(points)
    scale_coordinates(new_points, SCREEN_WIDTH, SCREEN_HEIGHT)
    graph = create_graph(new_points)
    profit_initial=f(initial_solution)
    gener_sol(solution_method, initial_solution, unvisited_points)
    return initial_solution ,unvisited_points,depot, Tmax
def calcule_timer_sol(solutionss,depo):
    f = 0
    for path  in solutionss:
        f += calcule_time_pathe(path ,depo)
    return f
def calcule_nmbr_ville_sol(sol, depot):
    cont = 0
    for j in sol:
        for i in j:
            if i.i != depot.i:
                cont += 1
    return cont + 1
def get_natural_number_from_input():
    
    try:
        value = int(input_fields[0]['text'])
        if value > 0:
            return value
        else:
            print("The value must be a natural number (greater than 0).")
            return None
    except ValueError:
        print("The input is not a valid integer.")
        return None
def import_data():
    global file_path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    root.destroy()
    if file_path:
        # تحديث قيمة file_path
        file_path = os.path.abspath(file_path)
        input_fields[3]['text'] = file_path
def repaire_solution(solution_supp, liste_non_visited, depot, Tmax):
    solutions = []
    for route in solution_supp:
        if calcule_time_pathe(route, depot) < Tmax:
            if route[-1].i == depot.i:
                route.pop(-1)
                path, liste_non_visite = repaire_fin(liste_non_visited, depot, Tmax, route)
                liste_non_visited = liste_non_visite
                solutions.append(path)
    udat = [loc.i for loc in liste_non_visited]
    print("udat",udat) 
    solution_finale = [[loc.i for loc in route] for route in solutions]
    print(f" la repert a la fin{solution_finale}")   
    return solutions, liste_non_visited
def enter_alns():
    # Initialize Pygame
    global initial_solution, unvisited_points,depot,Tmax


    # Colors
    WHITE = (255, 255, 255)
    BLUE_NUIT = (25, 25, 112)  # Dark blue color

    # Screen dimensions
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 750

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Generate Solution')

    # Load images
    return_button_image = pygame.image.load('photo/back (1).png')
    return_button_image = pygame.transform.scale(return_button_image, (50, 50))
    main_button_image = pygame.image.load('photo/home (1).png')
    main_button_image = pygame.transform.scale(main_button_image, (50, 50))  # Adjust size here
    background_image_path = os.path.join('photo', 'fond-ecran-colore-flou-artistique.jpg')
    background_image = pygame.image.load(background_image_path)

    # Fonts
    font = pygame.freetype.SysFont('segoe print', 24)
    small_font = pygame.freetype.SysFont('segoe print', 16)
    class Table:
        def __init__(self, headers, rows, x, y, widths, height, font):
            self.headers = headers
            self.rows = rows
            self.rect = pygame.Rect(x, y, sum(widths), height)
            self.widths = widths  # قائمة عرض الأعمدة
            self.font = font
        def draw(self, surface):
            cell_height = 30
            x_offset = self.rect.x

            # رسم العناوين
            for i, header in enumerate(self.headers):
                render_text(header, self.font, TEXT_COLOR, surface, x_offset, self.rect.y)
                x_offset += self.widths[i] if i < len(self.widths) else 0

            # رسم الصفوف
            y_offset = self.rect.y + cell_height
            for row in self.rows:
                x_offset = self.rect.x
                for i, cell in enumerate(row):
                    render_text(cell, self.font, TEXT_COLOR, surface, x_offset, y_offset)
                    x_offset += self.widths[i] if i < len(self.widths) else 0
                y_offset += cell_height


    # إعداد العناوين وعرض الأعمدة
    headers1 = ['Vehicle', 'Route', 'Profit', 'Route Time']
    widths1 = [100, 600, 150, 200]  # عرض الأعمدة بالترتيب
    headers2 = ['City', 'Profit', 'Arrival Time', 'Wait Time', 'Departure']
    widths2 = [100, 150, 400, 200, 400]  # عرض الأعمدة بالترتيب

    # إنشاء الجدولين باستخدام العناوين وعرض الأعمدة
    table1 = Table(headers1, [['', '', '', '']], 400, 180, widths1, 120, small_font)
    table2 = Table(headers2, [['', '', '', '', '']], 300, 420, widths2, 120, small_font)
    def render_text(text, font, color, surface, x, y):
        text_surface, rect = font.render(text, color)
        rect.topleft = (x, y)
        surface.blit(text_surface, rect)

    def return_to_lastpage():
        print("Returning to return_to_lastpage...")
        os.system('interface/solution_initial.py')  # Replace 'main_menu.py' with the actual script you want to run
        sys.exit()

    def return_to_main():
        print("Returning to main menu...")
        pygame.quit()
        os.system('interface/self_code.py')  # Replace 'main_menu.py' with the actual script you want to run
        sys.exit()

    class Button:
        def __init__(self, text, x, y, width, height, font, callback,args=None, image=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = WHITE
            self.font = font
            self.callback = callback
            self.args = args if args else []
            self.image = image

        def draw(self, surface):
            if self.image:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            else:
                pygame.draw.rect(surface, WHITE, self.rect, border_radius=15)
                pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=15)
                text_surface, rect = self.font.render(self.text, BLUE_NUIT)
                rect.center = self.rect.center
                surface.blit(text_surface, rect)


        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                if self.args:
                    self.callback(*self.args)
                else:
                    self.callback()

    return_button = Button('', SCREEN_WIDTH - 60, 10, 50, 50, font, return_to_lastpage, return_button_image)
    main_button = Button('', 1300, 10, 50, 50, font, return_to_main, main_button_image)  # Adjust size here

    # Input boxes
    input_boxes = [
        pygame.Rect(200, 20, 140, 32),  # max iteration

        pygame.Rect(1000, 20, 140, 32),  # number of segments
        pygame.Rect(1200, 670, 140, 32),  # total solution profit
        pygame.Rect(30, 670, 1160, 70)  # best solution form
    ]

    def get_input_values():
        global max_iteration,  segment
        
        try:
            max_iteration = int(input_texts[0])
            if max_iteration <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid positive integer for max iteration.")
            return False
        

        
        try:
            segment = int(input_texts[1])
            if segment <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid positive integer for number of segments.")
            return False
        
        return True
    # Tables

    input_texts = [''] * len(input_boxes)
    active_box = None
    best_solution=None
    profit_total=None
    def strart_algorithme():
        global initial_solution,best_solution,profit_total, file_de_solution,unvisited_points, max_iteration, segment, depot, Tmax
        
        # Call get_input_values and ensure it returns True before proceeding
        if not get_input_values():
            print("Invalid input values. Please correct the inputs.")
            return
        
        if initial_solution is None or unvisited_points is None:
            print("Initial solution or unvisited points are not available. Please generate an initial solution first.")
            return
        
        # Define your removal and repair operators
        D = [Worst_removal, Worst_removal_randome_y, random_removal,time_based_removal]
        R = [repaire_greedy, repaire_solution,shortest_path_insertion]

        # Call the ALNSv1 function
        best_solution, file_de_solution = ALNSv1(initial_solution, D, R, unvisited_points, max_iteration, segment, depot, Tmax)
        
        # Calculate the total profit
        profit_total = f(best_solution)
        
        # Update the best solution format
        udate = [[loc.i for loc in route] for route in best_solution]
        fil_best_solution = [[[loc.i for loc in route] for route in best_solution] for best_solution in file_de_solution]
        input_texts[3] = str(udate)
        input_texts[2] = str(profit_total)

        # Print results
        print("Best solution:", udate)
        print("Total profit:", profit_total)
        print("File de solution:", fil_best_solution)
# تحديث الجدول الأول ببيانات udate و best_solution
        while len(table1.rows) < len(udate):
            table1.rows.append(['', '', '', ''])
        for i in range(len(udate)):
            table1.rows[i][0] = str(i)  # تحديث العمود 'Vehicle'
            table1.rows[i][1] = str(udate[i])  # تحديث العمود 'Route'

            # تحديث الأعمدة 'Profit' و 'Route Time'
            table1.rows[i][2] = str(calculate_profit(best_solution[i]))  # تحديث العمود 'Profit'
            table1.rows[i][3] = str(calcule_time_pathe(best_solution[i], best_solution[i][0]))  # تحديث العمود 'Route Time'

        # تحديث الجدول الثاني بتفاصيل المدن
        for i in range(len(best_solution)):
            # التأكد من أن الجدول الثاني يحتوي على عدد كاف من الصفوف
            while len(table2.rows) < len(best_solution[i]):
                table2.rows.append(['', '', '', '', ''])
            
            for k in range(len(best_solution[i])):
                table2.rows[k][0] = str(best_solution[i][k].i)
                table2.rows[k][1] = str(best_solution[i][k].S)
                table2.rows[k][2] = str(best_solution[i][k].arrival_time)
                table2.rows[k][3] = str(wait_time(best_solution[i][k].arrival_time, best_solution[i][k].O))
                table2.rows[k][4] = str(best_solution[i][k].departure_time) 
    def dessin_best_sol(screen):
        global graph, best_solution,  clock, speed
        paths = read_solution(best_solution)
        build_edges(paths)
        update(paths, graph, screen)
    def dessin_toutes_best_solutions(screen):
        global graph, file_de_solution, clock, speed
        for i, best_solut in enumerate(file_de_solution):
            paths = read_solution(best_solut)
            build_edges(paths)
            update(paths, graph, screen)
            pygame.time.wait(100)
    def affiche_resulte():
        global profit_total,profit_initial,initial_solution,best_solution
        # Initialize Pygame
        pygame.init()

        # Set the dimensions of the window
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 700
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Simulation Result')

        # Load background image
        background_image_path = os.path.join('photo', 'fond-ecran-colore-flou-artistique.jpg')
        background_image = pygame.image.load(background_image_path)

        # Define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREY = (200, 200, 200)
        LIGHT_GREY = (220, 220, 220)
        BLUE = (0, 0, 255)
        NAVY_BLUE = (0, 0, 128)
        TEXT_COLOR = WHITE  # Change text color to white

        # Define fonts
        font = pygame.font.SysFont('segoeprint', 35)
        small_font = pygame.font.SysFont('segoeprint', 18)

        # Define a function to render text
        def render_text(text, font, color, surface, x, y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            surface.blit(text_surface, text_rect)

        class Table:
            def __init__(self, headers, rows, x, y, widths, height, font):
                self.headers = headers
                self.rows = rows
                self.rect = pygame.Rect(x, y, sum(widths), height)
                self.widths = widths  # Column widths
                self.font = font

            def draw(self, surface):
                cell_height = 30
                x_offset = self.rect.x

                # Draw headers
                for i, header in enumerate(self.headers):
                    render_text(header, self.font, TEXT_COLOR, surface, x_offset, self.rect.y)
                    x_offset += self.widths[i] if i < len(self.widths) else 0

                # Draw rows
                y_offset = self.rect.y + cell_height
                for row in self.rows:
                    x_offset = self.rect.x
                    for i, cell in enumerate(row):
                        render_text(cell, self.font, TEXT_COLOR, surface, x_offset, y_offset)
                        x_offset += self.widths[i] if i < len(self.widths) else 0
                    y_offset += cell_height

        headers1 = ["la solution", "profit", "le temps", "nombre de villes"]
        widths1 = [300, 300, 300, 300]  # Column widths

        # Create table instance
        table = Table(headers1, [['', '', '', '']], 100, 320, widths1, 120, small_font)
        while len(table.rows) < 2:
            table.rows.append(['', '', '', ''])

        # Populate the table rows
        for i in range(2):
            if i == 0:
                table.rows[i][0] = "solution initial"
                table.rows[i][1] = str(profit_initial)
                table.rows[i][2] = str(calcule_timer_sol(initial_solution, depot))
                table.rows[i][3] = str(calcule_nmbr_ville_sol(initial_solution, depot))
            else:
                table.rows[i][0] = "solution best"
                table.rows[i][1] = str(profit_total)
                table.rows[i][2] = str(calcule_timer_sol(best_solution, depot))
                table.rows[i][3] = str(calcule_nmbr_ville_sol(best_solution, depot))
        
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(background_image, (0, 0))
            
            # Render labels
            render_text("Le résultat de simulation :", font, WHITE, screen, 200, 25)
            render_text("La comparaison avec solution initiale et meilleure solution", font, (255, 0, 0), screen, 100, 560)
            render_text("the TOPTW with ALNS algorithme", font, WHITE, screen, 200, 70)
            # Draw table
            table.draw(screen)

            pygame.display.flip()

            #pygame.display.quit()
    
    
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('New Frame')

        



    # Buttons
    buttons = [
        Button('Start Algorithm', 20, 220, 200, 40, small_font,strart_algorithme),
        Button('Draw Best Solution', 20, 280, 200, 40, small_font,  display_graph, args=[SCREEN_WIDTH, SCREEN_HEIGHT,dessin_best_sol]),
        Button('Draw with Animation', 20, 360, 200, 40, small_font,  display_graph, args=[SCREEN_WIDTH, SCREEN_HEIGHT,dessin_toutes_best_solutions]),
        Button('Display Comparison', 20, 440, 200, 40, small_font, affiche_resulte)
    ]


    # Run until the user asks to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i
                        break
                else:
                    active_box = None
                return_button.handle_event(event)
                main_button.handle_event(event)
                for button in buttons:
                    button.handle_event(event)
            elif event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_texts[active_box] = input_texts[active_box][:-1]
                else:
                    input_texts[active_box] += event.unicode

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw labels
        labels = [
            ('Max Iteration', (20, 20)),
            ('Number of Segments', (800, 20)),
            ('Total Solution Profit:', (1200, 630)),
            ('Best Solution Form:', (20, 630))
        ]
        for text, pos in labels:
            render_text(text, small_font, WHITE, screen, pos[0], pos[1])

        # Draw input boxes
        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, WHITE, box, 0)
            pygame.draw.rect(screen, WHITE, box, 2)
            render_text(input_texts[i], small_font, BLUE_NUIT, screen, box.x + 5, box.y + 5)

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Draw return button
        return_button.draw(screen)
        main_button.draw(screen)

        # Draw tables
        table1.draw(screen)
        table2.draw(screen)

        # Update the display
        pygame.display.flip()

    #pygame.display.quit()
    
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('New Frame')


# دالة لإزالة عمود بالكامل (البيانات والرأس)
# دالة لإزالة عمود بالكامل (البيانات والرأس)
def remove_column(table, column_name):
    if column_name in table.headers:
        column_index = table.headers.index(column_name)
        original_columns[column_name] = [row[column_index] for row in table.rows]  # الاحتفاظ بالبيانات الأصلية
        table.headers.pop(column_index)
        for row in table.rows:
            row.pop(column_index)
# دالة لإعادة عمود بالكامل (البيانات والرأس) في الموقع الصحيح
def add_column(table, column_name, column_data, column_index):
    if column_name not in table.headers:
        table.headers.insert(column_index, column_name)
        for i in range(len(table.rows)):
            table.rows[i].insert(column_index, column_data[i] if i < len(column_data) else '')
# البيانات الأصلية للاحتفاظ بالبيانات الأصلية للأعمدة
original_columns = {}
# المواقع الأصلية للأعمدة
original_indices = {
    'route': 1,
    'profit': 2,
    'time de route': 3
}
def score_selected(checked):
    print(f"Insert Fin: {'Checked' if checked else 'Unchecked'}")
    if checked:
        print('check')
        add_column(tables[0], 'profit', original_columns.get('profit', ['' for _ in range(len(tables[0].rows))]), original_indices['profit'])
    else:
        remove_column(tables[0], 'profit')
def temp_selected(checked):
    print(f"Insert Gredy: {'Checked' if checked else 'Unchecked'}")
    if checked:
        print('check')
        add_column(tables[0], 'time de route', original_columns.get('time de route', ['' for _ in range(len(tables[0].rows))]), original_indices['time de route'])
    else:
        remove_column(tables[0], 'time de route')
box =None 
def insert_gredy(selected):
    global box
    print(f"Insert Gredy: {'Checked' if selected else 'Unchecked'}")
    box=None
    box='greedy'
    return box
def inser_fin(selected):
    global box
    print(f"Insert Fin: {'Checked' if selected else 'Unchecked'}")
    box=None
    box='inser_fin'
    return box
# Callback function for return button
def return_to_main():
    print("Returning to main menu...")
    pygame.quit()
    os.system('interface\self_code.py')  # Replace 'main_menu.py' with the actual script you want to run
    sys.exit()
# Callback functions for buttons and checkboxes
button_generate = Button('generate un solution', 30, 300, 200, 40, font, generate_initial_solution)
button_graph = Button('affiche le graphe', 30, 400, 200, 40, font, display_graph, args=[SCREEN_WIDTH, SCREEN_HEIGHT,dessine_sol_initial])
button_info_best = Button('enter info de ALNS', 30, 500, 200, 40, font, enter_alns)
return_button = Button('', SCREEN_WIDTH - 60, 10, 50, 50, font, return_to_main, return_button_image)
# Create labels
labels = [
    Label('entrer le nombre de vecule: <= 10', 30, 20, font),
    Label('choisir comment generir la solution initial:', 30, 60, font),
    Label('affiche les detaille de :', 30, 120, font),
    
    Label('affichage de detaille de ville:', 670, 140, font),
    Label('affichage de detaille de vecule:', 670, 390, font),
    Label('Total Solution Profit:', 1200, 630, font),
    Label('Best Solution Form:', 20, 630, font)
]
# Create checkboxes
checkboxes = [
    CheckBox('score', 400, 120, font, score_selected),
    CheckBox('temp', 550, 120, font, temp_selected)
]
# Create radiobuttons
radio_group = []
radiobuttons = [    
    RadioButton('insert_fin', 400, 60, font, radio_group, inser_fin),
    RadioButton('insert_gredy', 550, 60, font, radio_group, insert_gredy)
]
radiobuttons[1].selected = True  # Set 'temp' as selected by default
# Create tables
# tables = [
#     Table(['vecule', 'route', 'profit', 'time de route'], [['', '', '', '']], 400, 180, 700, 120, font),
#     Table(['ville', 'profite de ville', 'temp arriver', 'waite time','departure'], [['', '', '', '','']], 300, 420, 700, 120, font)
# ]
headers1 = ['Vehicle', 'Route', 'Profit', 'Route Time']
widths1 = [100, 600, 150, 200]  # عرض الأعمدة بالترتيب
headers2 = ['City', 'Profit', 'Arrival Time', 'Wait Time', 'Departure']
widths2 = [100, 150, 400, 200, 400]  # عرض الأعمدة بالترتيب
# إنشاء الجدولين باستخدام العناوين وعرض الأعمدة
tables = [Table(headers1, [['', '', '', '']], 400, 180, widths1, 120, font)
,Table(headers2, [['', '', '', '', '']], 300, 420, widths2, 120, font)]
# Create input fields
input_fields = [
    {'rect': pygame.Rect(350, 15, 200, 30), 'text': ''},
    {'rect': pygame.Rect(1200, 670, 140, 32), 'text': ''}, # total solution profit
    {'rect': pygame.Rect(30, 670, 1160, 70), 'text': 'solution_finale'}, # best solution form
    {'rect': pygame.Rect(680, 15, 500, 32), 'text': ''}
]
print(input_fields[1])
active_field = None
# Main loop
import_button = Button('', 600, 10, 50, 50, font, import_data, image=import_button_image)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, field in enumerate(input_fields):
                if field['rect'].collidepoint(event.pos):
                    active_field = i
                    break
            else:
                active_field = None
            button_generate.handle_event(event)
            button_graph.handle_event(event)
            button_info_best.handle_event(event)
            return_button.handle_event(event)
            import_button.handle_event(event)  # Handle events for the import button
            for radiobutton in radiobuttons:
                radiobutton.handle_event(event)
            for checkbox in checkboxes:
                checkbox.handle_event(event)
        elif event.type == pygame.KEYDOWN:
            if active_field is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_fields[active_field]['text'] = input_fields[active_field]['text'][:-1]
                else:
                    input_fields[active_field]['text'] += event.unicode

    screen.blit(background_image, (0, 0))

    # Draw buttons, labels, checkboxes, radiobuttons, and tables
    button_generate.draw(screen)
    button_graph.draw(screen)
    button_info_best.draw(screen)
    return_button.draw(screen)
    import_button.draw(screen)  # Draw the import button

    for label in labels:
        label.draw(screen)
    for checkbox in checkboxes:
        checkbox.draw(screen)
    for radiobutton in radiobuttons:
        radiobutton.draw(screen)
    for table in tables:
        table.draw(screen)

    # Draw input fields
    for field in input_fields:
        pygame.draw.rect(screen, WHITE, field['rect'])  # Fill with white background
        pygame.draw.rect(screen, TEXT_COLOR, field['rect'], 2)  # Draw border
        render_text(field['text'], font, BLUE_NUIT, screen, field['rect'].x + 5, field['rect'].y + 5)

    pygame.display.flip()
pygame.quit()
sys.exit()