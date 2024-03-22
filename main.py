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
GREEN = (5, 109, 0)
RED = (114, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (178, 183, 27)
ORANGE = (204, 138, 25)



window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

rect_menue = pygame.Rect(0, 0, WIN_WIDTH//2, WIN_HEIGHT//2)
rect_menue.center = (WIN_WIDTH//2, WIN_HEIGHT//2)

font = pygame.font.SysFont("Arial", 50)
txt_win = font.render("You win!", True, WHITE)
txt_win_rect = txt_win.get_rect(center = (WIN_WIDTH//2, WIN_HEIGHT//2-70))

txt_lose = font.render("You lose(", True, WHITE)
txt_lose_rect = txt_lose.get_rect(center = (WIN_WIDTH//2, WIN_HEIGHT//2-70))

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

btn_next = Button(rect_menue.x+rect_menue.width//10, rect_menue.centery+30, "Next Level", BLACK, GREEN)
btn_exit = Button(rect_menue.x+rect_menue.width*55//100, rect_menue.centery+30, "Exit", BLACK, ORANGE)
btn_restart = Button(rect_menue.x+rect_menue.width//10, rect_menue.centery+30, "Restart", BLACK, YELLOW)


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
        self.available = False
        
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

            elif lvl[row][col] == "r":
                obj = Fly(col*BLOCK, row*BLOCK+BLOCK//2, BLOCK, BLOCK//2, r"images\enemy_1.png", 2)
                enemies.add(obj)

            elif lvl[row][col] == "t":
                obj = Trumpline(col*BLOCK, row*BLOCK, BLOCK, BLOCK, r"images\jump 1.png")
                tramplines.add(obj)

    if not stars.sprites():
        flags.sprites()[0].available = True

create_level(map_1)

  

game = True
level = 1
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if isinstance(level, str):
            mouse_pos = pygame.mouse.get_pos()
            if btn_exit.rect.collidepoint(mouse_pos):
                btn_exit.active()
            else:
                btn_exit.deactive()

            if level == "win":
                if btn_next.rect.collidepoint(mouse_pos):
                    btn_next.active()
                else:
                    btn_next.deactive()

            elif level == "lose":
                if btn_restart.rect.collidepoint(mouse_pos):
                    btn_restart.active()
                else:
                    btn_restart.deactive()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_exit.rect.collidepoint(mouse_pos):
                        game = False
                    elif level == "win" and btn_next.rect.collidepoint(mouse_pos):
                        print("next lvl")
                    elif level == "lose" and btn_restart.rect.collidepoint(mouse_pos):
                        level = 1
                        create_level(map_1)                       
                        

    if level == 1:
        window.fill(BG)

        platforms.draw(window)
        player.draw(window)
        lava.draw(window)
        spikes.draw(window)
        stars.draw(window)
        LR_platforms.draw(window)
        UD_platforms.draw(window)
        enemies.draw(window)
        tramplines.draw(window)

        player.update()
        LR_platforms.update()
        UD_platforms.update()
        enemies.update()
        lava.update()
        spikes.update()
        tramplines.update()

        st_pl = pygame.sprite.groupcollide(stars, player, True, False)
        if st_pl:
            if not stars.sprites():
                flags.sprites()[0].available = True

        if flags.sprites()[0].available:
            flags.draw(window)
            flags.update()

        pl_tr = pygame.sprite.groupcollide(player, tramplines, False, False)
        if pl_tr:
            for pl in pl_tr:
                pl.gravity = -15
                pl.jumped = True
                pl_tr[pl][0].activate_tr()

        if pygame.sprite.groupcollide(player, flags, False, False):
            level = "win"

        if pygame.sprite.groupcollide(player, lava, False, False) \
            or pygame.sprite.groupcollide(player, spikes, False, False) \
            or  pygame.sprite.groupcollide(player, enemies,False, False):
                level = "lose"
    
    elif level == "win":
        pygame.draw.rect(window, GREEN, rect_menue)
        window.blit(txt_win, txt_win_rect)
        btn_next.show()
        btn_exit.show() 

    elif level == "lose":
        pygame.draw.rect(window, RED, rect_menue)
        window.blit(txt_lose, txt_lose_rect)
        btn_restart.show()
        btn_exit.show()

    clock.tick(FPS)
    pygame.display.update()

