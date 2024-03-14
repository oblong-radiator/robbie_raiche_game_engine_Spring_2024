# This file was created by Robbie Raiche

# game timer, different game levels, hp kills (stuff for thing)

# My first source control edit!!1!!1!!
# Import stuff
from random import randint
import sys
import pygame as pg
import settings as s
from sprites import *
from os import path
from math import floor
import time as t

class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# Creating the game class
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        pg.display.set_caption(s.TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        # added images folder and image in the load_data method for use with the player

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'fat_albert.png')).convert_alpha()
        self.map_data = []
        self.colrange = []
        self.rowrange = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                # print(line)
                self.map_data.append(line)
        
    def new(self):
        self.test_timer = Cooldown()
        print("create new game...")
        # init all variables, setup groups,instantiate classes.
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.collision = pg.sprite.Group()
        # for x in range (10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data): # drawing where the walls and player is at
            # print(row)
            # print(tiles)
            for col, tile in enumerate(tiles):
                # print(col)
                # print(tile)
                if tile == '1':
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self,col,row)
                if tile == "C":
                    Coin(self,col,row)
                if tile == "E":
                    self.colrange.append(col)
                    self.rowrange.append(row)

 # define the run method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(s.FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self): # x button works now
        pg.quit()
        sys.exit()

    def update(self): # UPDATE EVERYTHING!!
        self.test_timer.ticking()
        self.all_sprites.update()
        spawns = [7]
        while s.loaded_enemies < 5:
            spawn = randint(0,5)
            spawns.append(spawn)
            if spawn == spawns[-2]:
                break
            Enemy(self,self.colrange[spawn],self.rowrange[spawn])
            s.loaded_enemies += 1
            print(s.loaded_enemies)
            t.sleep(0.1)

    def draw_grid(self): # draw the grid with the tile size from settings
        for x in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (x, 0), (x, s.HEIGHT))
        for y in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (0, y), (s.WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*s.TILESIZE,y*s.TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self): # draw the background and the grid and all the sprites
        self.screen.fill(s.BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "COIN: " + str(self.player.coin), 64, s.YELLOW, 1, 1)
        self.draw_text(self.screen, "HP: " + str(self.player.hp), 64, s.LIGHTGREY, 1, 3)
        self.draw_text(self.screen, "TIME: " + str(floor((pg.time.get_ticks())/1000)), 32, s.WHITE, 15, 1)
        pg.display.flip()

    # define input methods
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_w:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_s:
            #         self.player.move(dy=1)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
    

g = Game()
# g.show_start_screen()
while True:
        g.new()
        g.run()
        # g.show_go_screen()
