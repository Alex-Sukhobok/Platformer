from typing import Any
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

class LeftRight(GameSprite):
    def __init__(self, x, y, width, height, picture, size_move):
        super().__init__(x, y, width, height, picture)
        self.direction = "right"
        self.min_co = self.rect.left - BLOCK * size_move
        self.max_co = self.rect.right + BLOCK * size_move

    
    def update(self):
        if self.direction == "right":
            self.rect.x += 1

        elif self.direction == "left":
            self.rect.x -= 1

        if self.rect.right >= self.max_co:
            self.direction = "left"

        if self.rect.left <= self.min_co:
            self.direction = "right"


class UpDown(GameSprite):
    def __init__(self, x, y, width, height, picture, size_move):
        super().__init__(x, y, width, height, picture)
        self.direction = "up"
        self.min_co = self.rect.top - BLOCK * size_move
        self.max_co = self.rect.bottom + BLOCK * size_move

    def update(self):
        if self.direction == "up":
            self.rect.y -= 1

        elif self.direction == "down":
            self.rect.y += 1

        if self.rect.bottom >= self.max_co:
            self.direction = "up"

        if self.rect.top <= self.min_co:
            self.direction = "down"



class Flag(GameSprite):
    def __init__ (self, x, y, width, height, picture):
        super().__init__(x, y, width, height, picture)
        self.image2 = pygame.image.load(file_path(r"images\flag2.png"))
        self.image2 = pygame.transform.scale(self.image2, (width, height))
        self.timer = 15
        self.images = [self.image, self.image2]
        self.pic_num = 0
        
    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.timer = 15

            self.pic_num += 1
            if self.pic_num == len(self.images):
                self.pic_num = 0
            self.image = self.images[self.pic_num]

class Fly(LeftRight):
    def __init__(self, x, y, width, height, picture, size_move):
        super().__init__(x, y, width, height, picture, size_move)
        image_l1 = pygame.image.load(file_path(r"images\enemy_1.png"))
        image_l1 = pygame.transform.scale(image_l1, (width, height))
        image_l2 = pygame.image.load(file_path(r"images\enemy_2.png"))
        image_l2 = pygame.transform.scale(image_l2, (width, height))
        self.images_l = [image_l1, image_l2]

        image_r1  = pygame.transform.flip(image_l1, True, False)
        image_r2  = pygame.transform.flip(image_l2, True, False)
        self.images_r = [image_r1, image_r2]

        self.timer = 10
        self.pic_num = 0

    def update(self):
        super().update()

        self.timer -= 1
        if self.timer == 0:
            self.timer = 10
            self.pic_num += 1
            if self.pic_num == len(self.images_r):
                self.pic_num = 0

        if self.direction == "right":
            self.image = self.images_r[self.pic_num]
        else:
            self.image = self.images_l[self.pic_num]
        

class Lava(GameSprite):
    def __init__(self, x, y, width, height, picture):
        super().__init__(x, y, width, height, picture)
        self.index = 0
        self.timer = 15
        self.image2 = pygame.transform.flip(self.image, True, False)
        self.images = [self.image, self.image2]

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.image = self.images[self.index]
            self.index += 1
            if self.index > 1:
                self.index = 0
            self.timer = 15

class Spikes(GameSprite):
    def __init__(self, x, y, width, height, picture):
        super().__init__(x, y, width, height, picture)
        self.index = 0
        self.timer = 90
        self.rect2 = pygame.Rect(x, int(y+2/3*height), width, int(height-1/3*height))
        self.image2 = pygame.transform.scale(self.image, (self.rect2.width, self.rect2.height))
        self.rects = [self.rect, self.rect2]
        self.images = [self.image, self.image2]

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.image = self.images[self.index]
            self.rect = self.rects[self.index]
            self.index += 1
            if self.index == 2:
                self.index = 0
            self.timer = 90


class Trumpline(GameSprite):
    def __init__(self, x, y, width, height, picture):
        super().__init__(x, y, width, height, picture)
        self.image1 = self.image   
        self.image2 = pygame.image.load(file_path(r"images\jump 2.png"))
        self.image2 = pygame.transform.scale(self.image2, (width, height))
        self.active = False
        self.timer = 50


    def activate_tr(self):
        self.active = True
        self.image = self.image2

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer == 0:
                self.image = self.image1
                self.active = False
                self.timer = 50


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
        move_check = True

        collide = pygame.sprite.spritecollide(self, blocks, False)
        if dy < 0:
            for obj in collide:
                self.rect.top = max(self.rect.top, obj.rect.bottom)
                self.gravity = 0
        elif dy >= 0:
            for obj in collide:
                self.rect.bottom = min(self.rect.bottom, obj.rect.top)
                self.groung = True

                if LR_platforms.has(obj) and move_check:
                    if obj.direction == "left":
                        self.rect.x -= 1
                    elif obj.direction == "right":
                        self.rect.x += 1
                    move_check = False

                elif UD_platforms.has(obj) and move_check:
                    if obj.direction == "up":
                        self.rect.y -= 1
                    move_check = False

        
        

        if self.rect.top <= 0:
            self.gravity = 0
    
        




map_1 = [
    "                  1                ",
    "                                   ",
    "                                   ",
    "             q                     ",
    "        00000000                   ",
    "                                   ",
    "                                   ",
    "   99                              ",
    "                                   ",
    "             2                     ",
    "       666   0000                  ",
    "                      777          ",
    "                                   ",
    "                               888 ",
    "                                   ",
    "                            4      ",
    "                        t 000      ",
    "        777            666         ",
    "     02222222000     t33        q  ",
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
'''
platforms = pygame.sprite.Group()
player = pygame.sprite.Group()
blocks = pygame.sprite.Group()
lava = pygame.sprite.Group()
spikes = pygame.sprite.Group()
stars = pygame.sprite.Group()
flags = pygame.sprite.Group()
LR_platforms = pygame.sprite.Group()
UD_platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
tramplines = pygame.sprite.Group()


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
        lava.draw(window)
        spikes.draw(window)
        stars.draw(window)
        flags.draw(window)
        LR_platforms.draw(window)
        UD_platforms.draw(window)
        enemies.draw(window)
        tramplines.draw(window)

        player.update()
        flags.update()
        LR_platforms.update()
        UD_platforms.update()
        enemies.update()
        lava.update()
        spikes.update()
        tramplines.update()

        pl_tr = pygame.sprite.groupcollide(player, tramplines, False, False)
        if pl_tr:
            for pl in pl_tr:
                pl.gravity = -20
                pl.jumped = True
                pl_tr[pl][0].activate_tr()

    clock.tick(FPS)
    pygame.display.update()

