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

class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, height, picture):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(picture))
        self.image = pygame.transform.scale(self.image, (width, height)) 

    def show(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, x, y, width, height, picture):
        super().__init__(x, y, width, height, picture)

    def update(self):
        pass 

map_1 = [
    "   0000     1     000              ",
    "                                   ",
    "                                   ",
    "                                   ",
    "           0000                    ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   ",
    "                                   "
]

'''
0 - platform
1 - player
'''
platforms = pygame.sprite.Group()
player = pygame.sprite.Group()

def create_level(lvl):
    platforms.empty()
    player.empty()
    
    for row in range(len(lvl)):
        for col in range(len(lvl[row])):
            if lvl[row][col] == "0":
                obj = GameSprite(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\ground 1.png")
                platforms.add(obj)

            elif lvl[row][col] == "1":
                obj = Player(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\I 1.png")
                player.add(obj)

create_level(map_1)



game = True
level = 1
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if level == 1:
        window.fill(BG)

        platforms.draw(window)
        player.draw(window)

        player.update()

    clock.tick(FPS)
    pygame.display.update()

