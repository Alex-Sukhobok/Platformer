from typing import Any
import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, file_name)
    return path

def level_path(number):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, "levels", str(number) + ".txt")
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
LIGHT_GREEN = (160, 255, 160)

# створення нового рівня 


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


class ButtonMenue():
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_light = pygame.font.SysFont("Arial", 25).render(text, True, BLACK)
        self.text_light_rect = self.text_light.get_rect(center=self.rect.center)
        self.text_bold = pygame.font.SysFont("Arial", 28, True).render(text, True, BLACK)
        self.text_bold_rect = self.text_bold.get_rect(center=self.rect.center)
        self.text = self.text_light
        self.text_rect = self.text_light_rect

    def show(self):
        pygame.draw.rect(window, WHITE, self.rect)
        window.blit(self.text, self.text_rect)

    def active(self):
        self.text = self.text_bold
        self.text_rect = self.text_bold_rect
    
    def deactive(self):
        self.text = self.text_light
        self.text_rect = self.text_light_rect


class CurrentTxtLvl():
    def __init__ (self, x, y, number):
        self.center = (x, y)
        self.change_text(number)

    def show (self):
        window.blit(self.text, self.text_rect)

    def change_text(self, number):
        text = str(number) + ".txt"
        self.text = pygame.font.SysFont("Arial", 30, True).render(text, True, LIGHT_GREEN)
        self.text_rect = self.text.get_rect(center=self.center)


class Level():
    def __init__(self):
        self.lvl_list = list()                  # список з з файлів "txt"
        self.num_lvl_list = list()              # список з номерів рівнів
        self.index_lvl = 0                      # порядковий індекс рівня у списку
        self.cur_lvl = None                     # номер рівня
        self.cut_txt_lvl = None                 # напис рівня на екрані
        self.lvl_map = list()                   # мапа рівня (список рядків)
        self.get_info(False)

    def get_info(self, saty_cur=True):
        self.lvl_list = os.listdir(file_path("levels"))
        if self.lvl_list:
            self.num_lvl_list = [int(num.replace(".txt", "")) for num in self.lvl_list]
            self.num_lvl_list.sort()    
            if saty_cur:
                self.index_lvl = self.num_lvl_list.index(self.cur_lvl)
                self.cut_txt_lvl.change_text(self.cur_lvl)
            else:
                self.cur_lvl = self.num_lvl_list[self.index_lvl]
                self.cut_txt_lvl = CurrentTxtLvl(GAME_WIDTH+120, 260, self.cur_lvl)        
                self.load_lvl()       
        else:
            self.num_lvl_list = []
            self.cur_lvl = 1
            self.cut_txt_lvl = CurrentTxtLvl(GAME_WIDTH+120, 260, 1)
            self.lvl_map = [" "*COL for i in range(ROW)]
        
    def load_lvl(self):
        path = level_path(self.cur_lvl)
        with open(path, encoding="utf-8") as file:
            self.lvl_map = file.read()            
            self.lvl_map = self.lvl_map.split("\n")
            self.lvl_map.pop(-1)

    def save_new_lvl(self):
        self.cur_lvl = 1
        while True:
            if self.cur_lvl in self.num_lvl_list:
                self.cur_lvl += 1
            else:
                break

        self.save_cur_lvl()
        self.get_info()


    def save_cur_lvl(self):
        path = level_path(self.cur_lvl)
        with open(path, "w", encoding="utf-8") as levels_txt:
            for row in self.lvl_map:
                levels_txt.write(row + "\n")
        
    def next_lvl(self):
        if self.index_lvl + 1 < len(self.num_lvl_list):
            self.index_lvl += 1
            self.cur_lvl = self.num_lvl_list[self.index_lvl]
            self.cut_txt_lvl.change_text(self.cur_lvl)
            self.load_lvl()

    def previous_lvl(self):
        if self.index_lvl > 0:
            self.index_lvl -= 1
            self.cur_lvl = self.num_lvl_list[self.index_lvl]
            self.cut_txt_lvl.change_text(self.cur_lvl)
            self.load_lvl()
            
    def show_clear_lvl(self):
        self.lvl_map = [" "*COL for i in range(ROW)]


level = Level()



  






new_button = ButtonMenue(GAME_WIDTH+30, 300, 180, 40, "New Level")
left_button = ButtonMenue(GAME_WIDTH+30, 360, 80, 40, "<")
right_button = ButtonMenue(GAME_WIDTH+130, 360, 80, 40, ">")
save_new_button = ButtonMenue(GAME_WIDTH+30, 420, 180, 40, "Save as new")
save_as_cur_button = ButtonMenue(GAME_WIDTH+30, 480, 180, 40, "Save as curent")


menue_btn_tuple = (new_button, left_button, right_button, save_new_button, save_as_cur_button)



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






class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, height, picture):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(picture))
        self.image = pygame.transform.scale(self.image, (width, height)) 

    def show(self):
        window.blit(self.image, self.rect)



'''
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

def show_pic(x, y, image):
    picture = pygame.image.load(file_path(image))
    picture = pygame.transform.scale(picture, (BLOCK, BLOCK))
    window.blit(picture, (x, y))

def show_level(new_map):
    
    for row in range(len(new_map)):
        for col in range(len(new_map[row])):
            if new_map[row][col] == "0":
                show_pic(col*BLOCK, row*BLOCK, r"images\ground 1.png")

            elif new_map[row][col] == "1":
                show_pic(col*BLOCK, row*BLOCK, r"images\I 1.png")
            
            elif new_map[row][col] == "2":
                show_pic(col*BLOCK, row*BLOCK, r"images\lava.png")
            
            elif new_map[row][col] == "3":
                show_pic(col*BLOCK, row*BLOCK, r"images\spikes.png")

            elif new_map[row][col] == "4":
                show_pic(col*BLOCK, row*BLOCK, r"images\star.png")

            elif new_map[row][col] == "5":
                show_pic(col*BLOCK, row*BLOCK, r"images\flag.png")
            
            elif new_map[row][col] == "6":
                show_pic(col*BLOCK, row*BLOCK, r"images\ground 3.png")
                
            elif new_map[row][col] == "7":
                show_pic(col*BLOCK, row*BLOCK, r"images\move_platform.png")
    
            elif new_map[row][col] == "8":
                show_pic(col*BLOCK, row*BLOCK, r"images\vmove_platform.png")

            elif new_map[row][col] == "9":
                show_pic(col*BLOCK, row*BLOCK, r"images\vmove2_pltfr.png")
            
            elif new_map[row][col] == "q":
                show_pic(col*BLOCK, row*BLOCK, r"images\slime.png")

            elif new_map[row][col] == "r":
                show_pic(col*BLOCK, row*BLOCK, r"images\enemy_1.png")

            elif new_map[row][col] == "t":
                show_pic(col*BLOCK, row*BLOCK, r"images\jump 1.png")



active_button = None

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEMOTION:
            cursor = event.pos
            for btn in menue_btn_tuple:
                if btn.rect.collidepoint(cursor):
                    btn.active()
                else:
                    btn.deactive()



        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor = event.pos
            x = cursor[0]//BLOCK
            y = cursor[1]//BLOCK
            
            if event.button == 1:
                if cursor[0] <= GAME_WIDTH and active_button:
                    level.lvl_map[y] = level.lvl_map[y][:x] + active_button.symbol + level.lvl_map[y][x+1:]
            
                else:
                    for obj in button_list:
                        if obj.rect.collidepoint(cursor):
                            obj.active = True
                            if active_button:
                                active_button.active = False
                            active_button = obj
                        
                    if new_button.rect.collidepoint(cursor):
                        level.show_clear_lvl()
                    elif left_button.rect.collidepoint(cursor):
                        level.previous_lvl()
                    elif right_button.rect.collidepoint(cursor):
                        level.next_lvl()
                    elif save_new_button.rect.collidepoint(cursor):
                        level.save_new_lvl()
                    elif save_as_cur_button.rect.collidepoint(cursor):
                        level.save_cur_lvl()
                        
                            

            elif event.button == 3:
                if cursor[0] <= GAME_WIDTH:
                    level.lvl_map[y] = level.lvl_map[y][:x] + " " + level.lvl_map[y][x+1:]
                

    window.fill(BG)
    pygame.draw.rect(window, GREY, editor_rect)
    show_level(level.lvl_map)
    mash()
    for btn in button_list:
        btn.show()

    for btn in menue_btn_tuple:
        btn.show()
    level.cut_txt_lvl.show()


    clock.tick(FPS)
    pygame.display.update()

