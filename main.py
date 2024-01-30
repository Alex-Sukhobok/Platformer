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
        self.gravity = 0
        self.jumped = False
        self.groung = False


    def update(self):
        dx, dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right < WIN_WIDTH:
            dx += 5
        if keys[pygame.K_a] and self.rect.left > 0:
            dx -= 5
        if keys[pygame.K_SPACE] and not self.jumped and self.groung:
            self.gravity = -12
            self.jumped = True
        if not keys[pygame.K_SPACE]:
            self.jumped = False

        self.gravity += 1
        if self.gravity > 10:
            self.gravity = 10
        dy += self.gravity

        self.rect.x += dx

        collide = pygame.sprite.spritecollide(self, blocks, False)
        if dx < 0:
            for obj in collide:
                self.rect.left = max(self.rect.left, obj.rect.right)
        elif dx > 0:
            for obj in collide:
                self.rect.right = min(self.rect.right, obj.rect.left)

        self.rect.y += dy
        
        self.groung = False

        collide = pygame.sprite.spritecollide(self, blocks, False)
        if dy < 0:
            for obj in collide:
                self.rect.top = max(self.rect.top, obj.rect.bottom)
                self.gravity = 0
        elif dy > 0:
            for obj in collide:
                self.rect.bottom = min(self.rect.bottom, obj.rect.top)
                self.groung = True

        if self.rect.top <= 0:
            self.gravity = 0
    
        




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
    "                          000      ",
    "                                   ",
    "     0                             ",
    "00000000000000000000000000000000000"
]

'''
0 - platform
1 - player
'''
platforms = pygame.sprite.Group()
player = pygame.sprite.Group()
blocks = pygame.sprite.Group()

def create_level(lvl):
    platforms.empty()
    player.empty()
    
    for row in range(len(lvl)):
        for col in range(len(lvl[row])):
            if lvl[row][col] == "0":
                obj = GameSprite(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\ground 1.png")
                platforms.add(obj)
                blocks.add(obj)

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

