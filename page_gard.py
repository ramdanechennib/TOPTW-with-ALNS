import subprocess
import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_size = (1000, 750)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Python Pygame Interface")

# Load and resize images
def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# Define the size for the button images
button_size = (50, 50)

# Load and resize car image
car_image = load_image("photo/3d-car.png", (30, 30))  # Assume you have a car image

# Load and resize location images
location_image = load_image("photo/pin.png", (30, 30))  # Assume you have a location image
location_car_image = load_image("photo/Sans titre.png", (700, 410)) # This is the image to be used as background for the white part with cars and locations

# Define colors
white = (255, 255, 255)
blue_nuit = (0, 0, 100) 

# Create button class
class Button:
    def __init__(self, x, y, text):
        self.image = pygame.Surface((150, 50))  # Create a white surface for the button
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.font = pygame.font.SysFont('segoeprint', 18)

        self.text_surface = self.font.render(text, True, blue_nuit)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.is_clicked = False
        self.click_animation_offset = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        surface.blit(self.text_surface, self.text_rect.topleft)

    def update(self):
        if self.is_clicked:
            self.click_animation_offset += 1
            if self.click_animation_offset > 5:
                self.click_animation_offset = -5
                self.is_clicked = False

    def click(self):
        self.is_clicked = True
        self.click_animation_offset = -5

# Create label class
class Label:
    def __init__(self, text, x, y, font_size, color=white, underline=False, bold=False):
        self.font = pygame.font.SysFont('segoeprint', font_size)
        if bold:
            self.font.set_bold(True)
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.underline = underline

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.x, self.y))
        if self.underline:
            text_rect = text_surface.get_rect(topleft=(self.x, self.y))
            underline_y = text_rect.bottom + 2  # Adjust this value to place the underline closer to the text
            pygame.draw.line(surface, self.color, (self.x, underline_y), (self.x + text_surface.get_width(), underline_y), 2)

# Create title labels
title_label1 = Label("Team Orienteering Problem with Time Windows", 30, 10, font_size=30, color=white, underline=False)
title_label3 = Label("with alns algorithme", 100, 50, font_size=30, color=white, underline=False)
# Create buttons and labels
button1 = Button(15, 500, "sumuler")
label2 = Label("encadrer par: ", 300, 650,20)
label4 = Label("Karoum Ali:        kerroum_ali@yahoo.fr", 500, 680,18 ,color=white, underline=True)

label5 = Label("Ramdane Chennib", 15, 200,20)
label6 = Label("ramdanechennib@gmail.com", 20, 230,18 ,color=white, underline=True)
label7 = Label("Chahine Kribaa", 15, 300,20)
label8 = Label("shaheenkribaa@gmail.com", 20, 330,18 ,color=white, underline=True)

buttons = [button1]

# Create car class
class Car:
    def __init__(self, x, y, path):
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1
        self.path = path
        self.path_index = 0

    def update(self):
        if self.path:
            target = self.path[self.path_index]
            if self.rect.topleft != target:
                if self.rect.x < target[0]:
                    self.rect.x += self.speed
                elif self.rect.x > target[0]:
                    self.rect.x -= self.speed
                if self.rect.y < target[1]:
                    self.rect.y += self.speed
                elif self.rect.y > target[1]:
                    self.rect.y -= self.speed
            else:
                self.path_index = (self.path_index + 1) % len(self.path)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Define locations
locations = [(700, 250), (430, 450), (380, 300), (840, 500), (850, 280), (550, 350), (750, 410)]
car_paths = [[random.choice(locations) for _ in range(5)] for _ in range(5)]

# Create cars with paths
cars = [Car(random.randint(0, window_size[0]), random.randint(0, window_size[1]), path) for path in car_paths]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    print("Button clicked!")
                    button.click()
                    if button == button1:
                        print("Running external script...")
                        pygame.quit()
                        subprocess.run(["python", "interface_jdida.py"])  # Replace 'your_script.py' with the actual script you want to run
                        sys.exit()

    # Update button animation
    for button in buttons:
        button.update()

    # Update car positions
    for car in cars:
        car.update()

    screen.fill(white)
    # Draw blue panel
    pygame.draw.rect(screen, blue_nuit, pygame.Rect(0, 0, 300, window_size[1]))
    pygame.draw.rect(screen, blue_nuit, pygame.Rect(0, 0, window_size[0], 190))
    pygame.draw.rect(screen, blue_nuit, pygame.Rect(0, 600, window_size[0], 150))

    # Draw title labels
    title_label1.draw(screen)
    title_label3.draw(screen)
    # Draw location_car_image as background for the white part with cars and locations
    screen.blit(location_car_image, (300, 190))  # Adjust the position as needed

    # Draw location images on blue panel
    for loc in locations:
        screen.blit(location_image, loc)

    # Draw cars on blue panel
    for car in cars:
        car.draw(screen)

    # Draw buttons and labels
    for button in buttons:
        button.draw(screen)
    label2.draw(screen)
    label4.draw(screen)
    label5.draw(screen)
    label6.draw(screen)
    label7.draw(screen)
    label8.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
