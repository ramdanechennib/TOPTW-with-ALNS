import pygame
import pygame.freetype
import os

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1540
screen_height = 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrollable Table with Pygame")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (169, 169, 169)

# Font
font_name = "Segoe Print"
font_size = 18
font = pygame.freetype.SysFont(font_name, font_size)

# Table dimensions
table_width = 600
table_height = 400
row_height = 30
col_widths = [200, 200, 200, 200]

# Scroll bar dimensions
scrollbar_width = 20

# Label padding
label_padding = 50  # Space reserved for the label

# X offset for the table and scrollbar
x_offset = 500  # Adjust this value as needed

# Function to extract file name from path
def extract_filename(path):
    return os.path.basename(path)

# Function to save data to file
def save_to_file(best_profit, nomber_veucule, initial_profit, path, filename="output.txt"):
    instance_name = extract_filename(path)
    
    # Check if the instance already exists in the file
    if not instance_exists(instance_name, nomber_veucule, initial_profit, best_profit, filename):
        with open(filename, "a") as file:  # Use "a" mode to append to the file if it exists
            file.write(f"{instance_name} | {nomber_veucule} | {initial_profit} | {best_profit}\n")

# Function to check if the instance already exists in the file
def instance_exists(instance_name, nomber_veucule, initial_profit, best_profit, filename="output.txt"):
    if not os.path.exists(filename):
        return False

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" | ")
            if len(parts) == 4:
                existing_instance_name, existing_nomber_veucule, existing_initial_profit, existing_best_profit = parts
                # Check if the instance_name and vehicle number match
                if (existing_instance_name == instance_name) and (existing_nomber_veucule == nomber_veucule):
                    return True
    return False

# Function to read data from file
def read_from_file(filename="output.txt"):
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(" | ")
                if len(parts) == 4:
                    instance_name, nomber_veucule, initial_profit, best_profit = parts
                    data.append([instance_name, nomber_veucule, initial_profit, best_profit])
    return data

# Function to display the table with given data
def display_table(best_profit, nomber_veucule, initial_profit, path):
    save_to_file(best_profit, nomber_veucule, initial_profit, path)

    # Read the data from the file
    data = read_from_file("output.txt")

    headers = ["Instance", "nomber veucule", "Profit Initial", "Profit Final"]

    # Set to keep track of displayed instances
    displayed_instances = set()

    # Scroll position
    scroll_y = 0
    max_scroll_y = 0

    # Scrollbar state
    scrolling = False
    scrollbar_rect = pygame.Rect(0, label_padding, scrollbar_width, 0)

    # Table data initialization
    table_data = [headers]

    # Function to add new instance data if not already displayed
    def add_instance_data(instance):
        if (instance[0], instance[1]) not in displayed_instances:
            table_data.append(instance)
            displayed_instances.add((instance[0], instance[1]))

    # Function to draw the entire screen
    def draw_screen():
        # Clear screen
        screen.fill(GRAY)

        # Draw label
        font.render_to(screen, (10, 150), "affichage de toute les comparesant qui deja tester", BLACK)

        # Draw table data with transparency
        for row_idx, row in enumerate(table_data):
            row_y = 50 - scroll_y + (row_idx + 1) * row_height

            # Calculate transparency factor based on the row's position relative to the line at y = 110
            if row_y >= 110:
                transparency = 255
            else:
                transparency = max(0, int(255 * (row_y / 110)))

            # Render each cell in the row with transparency
            for col_idx, item in enumerate(row):
                # Create a surface for each cell's text
                text_surface, _ = font.render(item, BLACK)

                # Ensure text_surface is not None and then set transparency
                if text_surface:
                    text_surface.set_alpha(transparency)

                    # Blit the text surface onto the main screen
                    screen.blit(text_surface, (col_idx * col_widths[col_idx] + 5 + x_offset, row_y + 5))

        # Draw scrollbar background
        pygame.draw.rect(screen, GRAY, (table_width + x_offset, 50, scrollbar_width, screen_height - 50))

        # Draw scrollbar handle
        if max_scroll_y > 0:
            handle_height = (screen_height - 50) * ((screen_height - 50) / ((len(table_data) + 1) * row_height))
            handle_pos_y = 50 + (scroll_y / max_scroll_y) * ((screen_height - 50) - handle_height)
            scrollbar_rect.x = table_width + 800
            scrollbar_rect.y = handle_pos_y
            scrollbar_rect.height = handle_height
            pygame.draw.rect(screen, BLACK, scrollbar_rect)

        # Update display
        pygame.display.flip()

    # Add instance data initially
    for instance in data:
        add_instance_data(instance)
    max_scroll_y = max(0, (len(table_data) + 1) * row_height - table_height - label_padding)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if scrollbar_rect.collidepoint(event.pos):
                        scrolling = True
                        mouse_y_start = event.pos[1]
                        scroll_start = scroll_y
                elif event.button == 4:  # Scroll up
                    scroll_y = max(scroll_y - row_height, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = min(scroll_y + row_height, max_scroll_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    scrolling = False
            elif event.type == pygame.MOUSEMOTION:
                if scrolling:
                    mouse_y = event.pos[1]
                    dy = mouse_y - mouse_y_start
                    scroll_y = min(max(scroll_start + dy * (max_scroll_y / (screen_height - 50 - scrollbar_rect.height)), 0), max_scroll_y)

        draw_screen()


# Example usage
nomber_veucule = "5ممك4"
best_profit = "Bt Profit Example"
initial_profit = "Initial Profit Example"
path = r"C:\\Users\\ramdan chennib\\Pictures\\memoir ramdane\\instance\\c_r_rc_100_50\\c109.txt"

display_table(best_profit, nomber_veucule, initial_profit, path)
pygame.quit()
