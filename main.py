import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, file_name)
    return path

BLOCK = 30
WIN_WIDTH = BLOCK * 35
WIN_HEIGHT = BLOCK * 20
FPS = 40
BG = (0, 0, 0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

game = True
level = 1
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            game = False

    if level == 1:
        window.fill(BG)

    clock.tick(FPS)
    pygame.display.update()

