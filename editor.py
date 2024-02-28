from typing import Any
import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, file_name)
    return path

BLOCK = 30
ROW = 20
COL = 35
WIN_WIDTH = BLOCK * COL + 8 * BLOCK
WIN_HEIGHT = BLOCK * ROW
GAME_WIDTH = BLOCK * COL
FPS = 40
BG = (0, 0, 0)
GREEN = (5, 109, 0)
RED = (114, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (178, 183, 27)
ORANGE = (204, 138, 25)
GREY = (71, 71, 71)



window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
editor_rect = pygame.Rect(GAME_WIDTH, 0, BLOCK*8, WIN_HEIGHT)

def mash():
    for i in range(COL+1):
        pygame.draw.line(window, WHITE, (i*BLOCK, 0), (i*BLOCK, WIN_HEIGHT))
    for i in range(ROW+1):
        pass

class Button():
    def __init__(self, x, y, text, color1, color2):
        self.rect = pygame.Rect(x, y, WIN_WIDTH//200*35, 50)
        self.color = color1
        self.color_deactive = color1
        self.color_active = color2
        self.text = pygame.font.SysFont("Arial", 30).render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center = self.rect.center)

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, self.text_rect)

    def active(self):
        self.color = self.color_active

    def deactive(self):
        self.color = self.color_deactive



class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, height, picture):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(picture))
        self.image = pygame.transform.scale(self.image, (width, height)) 

    def show(self):
        window.blit(self.image, self.rect)




map_1 = [
    "                  1                ",
    "                         000       ",
    "                      3            ",
    "             q      000000         ",
    "        00000000           888     ",
    "                                   ",
    "                                   ",
    "   99                              ",
    "             2                     ",
    "             0000           000    ",
    "       666                         ",
    "                     7777          ",
    "                                   ",
    "                               888 ",
    "                                   ",
    "                            t      ",
    "                       5  000      ",
    "        777    4       66          ",
    "     02222222220      33       q   ",
    "00000000000000000000000000000000000"
]

'''
0 - platform
1 - player
2 - lava
3 - spikes
4 - stars
5 - flag
6 - LR one point
7 - LR two point
8 - UD one point
9 - UD two point
q - enemy LR one point
r - enemy LR two point
t - trampline




def create_level(lvl):
    platforms.empty()
    player.empty()
    lava.empty()
    spikes.empty()
    stars.empty()
    flags.empty()
    LR_platforms.empty()
    UD_platforms.empty()
    enemies.empty()
    tramplines.empty()

    
    for row in range(len(lvl)):
        for col in range(len(lvl[row])):
            if lvl[row][col] == "0":
                obj = GameSprite(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\ground 1.png")
                platforms.add(obj)
                blocks.add(obj)

            elif lvl[row][col] == "1":
                obj = Player(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\I 1.png")
                player.add(obj)

            elif lvl[row][col] == "2":
                obj = Lava(col*BLOCK, row*BLOCK+5, BLOCK, BLOCK-5, r"images\lava.png")
                lava.add(obj)

            elif lvl[row][col] == "3":
                obj = Spikes(col*BLOCK, row*BLOCK+5, BLOCK, BLOCK-5, r"images\spikes.png")
                spikes.add(obj)

            elif lvl[row][col] == "4":
                obj = GameSprite(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\star.png")
                stars.add(obj)

            elif lvl[row][col] == "5":
                obj = Flag(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\flag.png")
                flags.add(obj)

            elif lvl[row][col] == "6":
                obj = LeftRight(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\ground 3.png", 1)
                LR_platforms.add(obj)
                blocks.add(obj)

            elif lvl[row][col] == "7":
                obj = LeftRight(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\move_platform.png", 2)
                LR_platforms.add(obj)
                blocks.add(obj)

            elif lvl[row][col] == "8":
                obj = UpDown(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\vmove_platform.png", 1)
                UD_platforms.add(obj)
                blocks.add(obj)

            elif lvl[row][col] == "9":
                obj = UpDown(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\vmove2_pltfr.png", 2)
                UD_platforms.add(obj)
                blocks.add(obj)

            elif lvl[row][col] == "q":
                obj = LeftRight(col*BLOCK, row*BLOCK+BLOCK//2, BLOCK, BLOCK//2, r"images\slime.png", 1)
                enemies.add(obj)

            elif lvl[row][col] == "e":
                obj = Fly(col*BLOCK, row*BLOCK+BLOCK//2, BLOCK, BLOCK//2, r"images\enemy_1.png", 2)
                enemies.add(obj)

            elif lvl[row][col] == "t":
                obj = Trumpline(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\jump 1.png")
                tramplines.add(obj)

    if not stars.sprites():
        flags.sprites()[0].available = True
'''  

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill(BG)
    pygame.draw.rect(window, GREY, editor_rect)
    mash()    
    clock.tick(FPS)
    pygame.display.update()

