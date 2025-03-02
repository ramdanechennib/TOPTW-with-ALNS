import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog
from comparaisant_all import display_table
from destruction import Worst_removal, Worst_removal_randome_y, random_removal, time_based_removal
from location import Location
import subprocess
from alns import ALNSv1, f
from les_fun_interface import build_edges, create_graph, display_initial_solution, generate_solution, read_input_data, read_solution, scale_coordinates, travel_time, update, wait_time
from generate_solution import create_solution
from affiche_result import affiche_result # type: ignore
from repair import calculate_profit, calcule_time_pathe, repaire_fin, repaire_greedy, shortest_path_insertion
import copy

pygame.init()

# إعدادات الشاشة
screen = pygame.display.set_mode((1540, 780))
pygame.display.set_caption("NewJFrame")
SCREEN_WIDTH = 1540
SCREEN_HEIGHT = 780
# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200, 128)
LIGHT_GREY = (180, 180, 180)
BLUE = (0, 0, 255)
NAVY_BLUE = (0, 0, 128)
BLUE_NUIT = (0, 0, 50)
TEXT_COLOR = BLACK
# إعداد الخطوط
font = pygame.freetype.SysFont('segoe print', 24)
small_font = pygame.freetype.SysFont('segoe print', 16)
font = pygame.font.SysFont('segoe print', 16) 
file_path = None
max_iteration = None
initial_temperature = None
segment = None
initial_solution = None
unvisited_points = None
depot = None
Tmax = None
graph = None
solution_method = None
file_de_solution=None
travel_time_initiall=None
initiall_sol_id=None
best_solution=None
travel_time_finall=None
best_sol_id=None
profite_best=None
time_initiall_pathe=None
profite_initiall_pathe=None
time_initiall_pathe=None
profite_initiall_pathe=None
number_of_paths=None

graphe=None

# دوال لرسم النصوص والمستطيلات الدائرية
def render_text(text, font, color, surface, x, y, background=None):
    text = str(text)  # Ensure the text is a string
    if background is not None:
        textobj = font.render(text, True, color, background)
    else:
        textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# فئة الأزرار
class Button:
    def __init__(self, text, x, y, width, height, font, callback, args=None, image=None, visible=True):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.font = font
        self.callback = callback
        self.args = args if args else []
        self.corner_radius = 15
        self.image = image
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            if self.image:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            else:
                draw_rounded_rect(surface, self.color, self.rect, self.corner_radius)
                text_surface = self.font.render(self.text, True, WHITE)
                text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
                surface.blit(text_surface, text_rect.topleft)

    def handle_event(self, event):
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback(*self.args)

class RadioButton:
    def __init__(self, text, x, y, font, group, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = BLACK
        self.font = font
        self.selected = False
        self.group = group
        self.callback = callback
        group.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.x + 10, self.rect.y + 10), 10, 2)
        if self.selected:
            pygame.draw.circle(surface, BLUE_NUIT, (self.rect.x + 10, self.rect.y + 10), 5)
        render_text(self.text, self.font, BLACK, surface, self.rect.x + 25, self.rect.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                for radio in self.group:
                    radio.selected = False
                self.selected = True
                self.callback(self.selected)

# فئة العلامات
class Label:
    def __init__(self, text, x, y, font):
        self.text = text
        self.font = font
        self.x = x
        self.y = y

    def draw(self, surface):
        render_text(self.text, self.font, BLACK, surface, self.x, self.y)

def get_vuecule_number_from_input():
    try:
        value = int(input_boxes["num_vehicles"]['text'])
        if value > 0:
            return value
        else:
            print("The value must be a natural number (greater than 0).")
            return None
    except ValueError:
        print("The input is not a valid integer.")
        return None
def get_segment_number_from_input():
    try:
        value = int(input_boxes["num_segments"]['text'])
        if value > 0:
            return value
        else:
            print("The value must be a natural number (greater than 0).")
            return None
    except ValueError:
        print("The input is not a valid integer.")
        return None
def get_iteration_number_from_input():
    try:
        value = int(input_boxes["num_iterations"]['text'])
        if value > 0:
            return value
        else:
            print("The value must be a natural number (greater than 0).")
            return None
    except ValueError:
        print("The input is not a valid integer.")
        return None
def insert_fin(selected):
    global solution_method
    solution_method=None
    solution_method = 'inser_fin'
    print(f"Insert Fin: {'Checked' if selected else 'Unchecked'}, solution_method: {solution_method}")
    return solution_method

def insert_greedy(selected):
    global solution_method
    solution_method=None
    solution_method = 'greedy'
    print(f"Insert Greedy: {'Checked' if selected else 'Unchecked'}, solution_method: {solution_method}")
    return solution_method

def insert_time(selected):
    global solution_method
    solution_method=None
    solution_method = 'inser_time'
    print(f"Insert Time: {'Checked' if selected else 'Unchecked'}, solution_method: {solution_method}")
    
    return solution_method

radio_group = []
radiobuttons = [
    RadioButton('insert_fin', 50, 110, font, radio_group, insert_fin),
    RadioButton('insert_greedy', 250, 110, font, radio_group, insert_greedy),
    RadioButton('insert_time', 550, 110, font, radio_group, insert_time)
]
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
# تعريف دوال الاستدعاء
def travel_time_solution(solution):
    travel_time_list = []
    time_pathe=[]
    profite_pathe=[]
    for path in solution:

        time_pathe.append(calcule_time_pathe(path, path[0]))
        profite_pathe.append(calculate_profit(path))
        # print ("profite_pathe",profite_pathe)
        for i in range(len(path) - 1):
            travel_time_list.append(path[i].i)
            travel_time_list.append(path[i+1].i)
              # Use range(len(path) - 1) to avoid IndexError
            travel_time_list.append(travel_time(path[i], path[i+1]))
    return travel_time_list,time_pathe,profite_pathe
filename="output.txt"

def generate_solutio():
    global number_of_paths,filename,initial_solution,file_de_solution, profit_initial, unvisited_points, solution_method, depot, Tmax, points, file_path, graph,travel_time_initiall,initiall_sol_id,time_initiall_pathe,profite_initiall_pathe
    global graphe,graph,best_solution,travel_time_finall,best_sol_id,profite_best,time_finall_pathe,profite_finall_pathe
    print("Generating solution...")
    for button in remaining_buttons:
        button.visible = True

    if file_path is None:
        print("No file selected. Please import a data file first.")
        return
    
    print(f"Selected solution method: {solution_method}")  # طباعه القيمة الحالية لـ solution_method
    
    if solution_method == "inser_fin":
        print("FIN selected")
    elif solution_method == "greedy":
        print("GREEDY selected")
    elif solution_method == "inser_time":
        print("TIME selected")
    else:
        print("No option selected")
        return  # إضافة شرط إنهاء عند عدم اختيار أي خيار

    print('file_path', file_path)
    print('initial_solution', initial_solution)
    
    number_of_paths = get_vuecule_number_from_input()
    max_iteration = get_iteration_number_from_input()
    print ("num_iterations",max_iteration)
    segment = get_segment_number_from_input()
    if number_of_paths is None:
        print("Please enter a valid natural number for the number of paths.")
        return
    print('number_of_paths', number_of_paths)
    
    initial_solution, unvisited_points, solution_method, points, depot, Tmax = generate_solution(file_path, solution_method, number_of_paths)

    travel_time_initiall,time_initiall_pathe,profite_initiall_pathe=travel_time_solution(initial_solution)
    print ("travel_time_initiall",travel_time_initiall)
    # print('initial_solution', initial_solution)

    profit_initial = f(initial_solution)
    initiall_sol_id = [[loc.i for loc in route] for route in initial_solution]
    print("best_solution",initiall_sol_id)
    print("profit_initial",profit_initial)
    D = [Worst_removal, Worst_removal_randome_y, random_removal,time_based_removal]
    R = [repaire_greedy, repaire_solution,shortest_path_insertion]

    # Call the ALNSv1 function
    best_solution, file_de_solution = ALNSv1(initial_solution, D, R, unvisited_points, max_iteration, segment, depot, Tmax)
    travel_time_finall , time_finall_pathe,profite_finall_pathe=travel_time_solution(best_solution)
    print ("travel_time_finall",travel_time_finall)
    # Calculate the total profit
    profite_best = f(best_solution)
    best_sol_id = [[loc.i for loc in route] for route in best_solution]
    print("best_solution",best_sol_id)
    print("profite final",profite_best)
    # إظهار الأزرار المتبقية عند الضغط على زر generate
    new_points = copy.deepcopy(points)
    scale_coordinates(new_points, SCREEN_WIDTH, SCREEN_HEIGHT)
    graph = create_graph(new_points)
    return best_solution,initial_solution, travel_time_initiall ,travel_time_finall,best_sol_id,initiall_sol_id,profit_initial,profite_best,time_finall_pathe,profite_finall_pathe,time_initiall_pathe,profite_initiall_pathe
initial="initial"
fin='fin'
def show_initial():
    global graph,initial_solution, travel_time_initiall,initiall_sol_id,profit_initial,time_initiall_pathe,profite_initiall_pathe
    affiche_result(initial_solution, travel_time_initiall,initiall_sol_id,profit_initial,initial,graph)
    print ("travel_time_initialltravel_time_initiall",travel_time_initiall)
    print("Showing initial...")

def show_best():
    global graph,best_solution,travel_time_finall,best_sol_id,profite_best,time_finall_pathe,profite_finall_pathe
    affiche_result(best_solution, travel_time_finall,best_sol_id,profite_best,fin,graph)
    print ("travel_time_finalltravel_time_finall",travel_time_finall)
    print("Showing best...")
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

def compare():
        print("Comparing...")

        global profite_best,profit_initial,initial_solution,best_solution
        # Initialize Pygame
        pygame.init()

        # Set the dimensions of the window
        SCREEN_WIDTH = 1540
        SCREEN_HEIGHT = 780
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
                table.rows[i][1] = str(profite_best)
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


def show_all_comparisons():
    global file_path ,profite_best,profit_initial,number_of_paths
    print("Showing all comparisons...")
    path=file_path
    display_table(str(profite_best),str(number_of_paths), str(profit_initial),str( path))

def quit():
    pygame.quit()
    sys.exit()

def print_pdf():
    print("Printing PDF...")

def import_data():
    print("Importing data...")
    global file_path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    root.destroy()
    if file_path:
        # تحديث قيمة file_path
        file_path = os.path.abspath(file_path)
        input_boxes["file_path"]['text'] = file_path
    # إظهار زر generate عند الضغط على زر import
    button_generate.visible = True
    

# إعداد الأزرار
button_generate = Button('generate', 100, 600, 130, 30, font, generate_solutio, visible=False)
button_show_initial = Button('show_initial', 300, 600, 130, 30, font, show_initial, visible=False)
button_show_best = Button('show_best', 500, 600, 150, 30, font, show_best, visible=False)
button_compare = Button('compare', 680, 600, 130, 30, font, compare, visible=False)
button_show_all_comparisons = Button('show all comparisons', 840, 600, 280, 30, font, show_all_comparisons, visible=False)
button_quit = Button('quit', 1300, 600, 100, 30, font, quit, visible=False)
button_print_pdf = Button('print PDF', 1150, 600, 120, 30, font, print_pdf, visible=False)

remaining_buttons = [
    button_show_initial, button_show_best, button_compare, button_show_all_comparisons, button_quit, button_print_pdf
]

buttons = [
    button_generate
]

# بديل لصورة استيراد البيانات
import_button_image = pygame.image.load('photo/txt-file-format.png')
import_button_image = pygame.transform.scale(import_button_image, (50, 50))
import_button = Button('', 20, 20, 50, 50, font, import_data, image=import_button_image)
buttons.append(import_button)

# إعداد مجموعة الأزرار الراديوية

# إعداد العلامات
labels = [
    Label("choisire comment genirer la solution initial:", 20, 70, font),
    Label("entrer le nombre de vecule :<=10", 20, 200, font),
    Label("le nomber de segment", 20, 300, font),
    Label("le nomber des iteration", 20, 400, font),
]

# إعداد الحقول النصية
input_boxes = {
    "file_path": {"rect": pygame.Rect(160, 20, 700, 30), "text": "", "active": False},
    "num_vehicles": {"rect": pygame.Rect(550, 200, 100, 30), "text": "", "active": False},
    "num_segments": {"rect": pygame.Rect(550, 300, 100, 30), "text": "", "active": False},
    "num_iterations": {"rect": pygame.Rect(550, 400, 100, 30), "text": "", "active": False}
}

# تشغيل البرنامج
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.handle_event(event)
            for button in remaining_buttons:
                button.handle_event(event)
            for radiobutton in radiobuttons:
                radiobutton.handle_event(event)
            for key, box in input_boxes.items():
                if box["rect"].collidepoint(event.pos):
                    box["active"] = True
                else:
                    box["active"] = False
        elif event.type == pygame.KEYDOWN:
            for key, box in input_boxes.items():
                if box["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        box["text"] = box["text"][:-1]
                    else:
                        box["text"] += event.unicode
    if pygame.display.get_surface() is not None:
            screen.fill(WHITE)
    

            # رسم العلامات
            for label in labels:
                label.draw(screen)

            # رسم الأزرار
            for button in buttons:
                button.draw(screen)
            
            # رسم الأزرار المتبقية
            for button in remaining_buttons:
                button.draw(screen)
            
            # رسم الأزرار الراديوية
            for radiobutton in radiobuttons:
                radiobutton.draw(screen)

            # رسم الحقول النصية
            for key, box in input_boxes.items():
                pygame.draw.rect(screen, LIGHT_GREY if box["active"] else WHITE, box["rect"])  # Fill with background
                pygame.draw.rect(screen, TEXT_COLOR, box["rect"], 2)  # Draw border
                render_text(box["text"], font, BLUE_NUIT, screen, box["rect"].x + 5, box["rect"].y + 5)

            pygame.display.flip()
    else:
            print("Display surface is no longer available.")
            running = False

pygame.quit()
