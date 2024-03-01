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
        pygame.draw.line(window, WHITE, (0, i*BLOCK), (GAME_WIDTH, i*BLOCK))

class Button():
    def __init__(self, x, y, image, symbol):
        self.rect = pygame.Rect(x, y, BLOCK, BLOCK)
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (BLOCK, BLOCK))
        self.symbol = symbol
        self.active = False

    def show(self):
        window.blit(self.image, self.rect)
        if self.active:
            pygame.draw.rect(window, RED, self.rect, 3)
        
objects_dict = {
    "0" : r"images\ground 1.png",
    "1" : r"images\I 1.png",
    "2" : r"images\lava.png",
    "3" : r"images\spikes.png",
    "4" : r"images\star.png",
    "5" : r"images\flag.png",
    "6" : r"images\ground 3.png",
    "7" : r"images\move_platform.png",
    "8" : r"images\vmove_platform.png",
    "9" : r"images\vmove2_pltfr.png",
    "q" : r"images\slime.png",
    "r" : r"images\enemy_1.png",
    "t" : r"images\jump 1.png"

}

button_list = []

x = 20
y = 20
num_btn = 0
for key, value in objects_dict.items():
    button = Button(GAME_WIDTH+x, y, value, key)
    x += BLOCK + 15
    button_list.append(button)
    num_btn += 1
    if num_btn == 5:
        y += BLOCK + 10
        x = 20
        num_btn = 0

'''
btn_col, btn_row = 1, 1
for key, value in objects_dict.items():
    button = Button(GAME_WIDTH+BLOCK*btn_col*1.2, BLOCK*btn_row*1.3, value, key)
    button_list.append(button)
    btn_col += 1
    if btn_col == 6:
        btn_col = 1
        btn_row += 1
'''

new_map = [" "*COL for i in range(ROW)]


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




def show_level(lvl):
    

    
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
    for btn in button_list:
        btn.show()

    clock.tick(FPS)
    pygame.display.update()

