# This file was created by Robbie Raiche

# game timer, random enemy spawning, level change system

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

LEVEL1 = "map.txt"
LEVEL2 = "maplv2.txt"

# Creating the game class
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        pg.display.set_caption(s.TITLE)
        self.running = True
        self.paused = False
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        
        # added images folder and image in the load_data method for use with the player


    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        # self.player_img = pg.image.load(path.join(self.img_folder, 'fat_albert.png')).convert_alpha()
        self.map_data = []
        self.colrange = []
        self.rowrange = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
            self.level = 1
            for line in f:
                # print(line)
                self.map_data.append(line)

    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        self.map_data = [] # reset map_data to empty
        s.loaded_enemies = 0
        with open(path.join(self.game_folder, lvl), 'rt') as f: #open level
            for line in f:
                print(line)
                self.map_data.append(line)
        for row, tiles in enumerate(self.map_data): # drawing where the walls and player is at
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self,col,row)
                if tile == "C":
                    Coin(self,col,row)
                if tile == "E":
                    self.colrange.append(col)
                    self.rowrange.append(row)
        
    def new(self):
        print("create new game...")
        # init all variables, setup groups,instantiate classes.
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.collision = pg.sprite.Group()
        self.elevators = pg.sprite.Group()
        self.elevator = 0
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
        if not self.paused:
            self.all_sprites.update()
            spawns = [7]
            if self.player.coin == 8:
                self.show_end_screen()
            if self.player.hp <= 0:
                self.show_death_screen()
            while s.loaded_enemies < 3:
                spawn = randint(0,5)
                spawns.append(spawn)
                if spawn == spawns[-2]:
                    break
                Enemy(self,self.colrange[spawn],self.rowrange[spawn])
                s.loaded_enemies += 1
                print(s.loaded_enemies)
            if s.inelevator == True:
                self.change_level(LEVEL2)
                self.level = 2
                s.inelevator = False
            if self.level == 1:
                if self.elevator == 0:
                    if self.player.coin == 4:
                        Elevator(self,30,12)
                        self.elevator = 1
                        print("elevator spawned") 

    def draw_grid(self): # draw the grid with the tile size from settings
        for x in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (x, 0), (x, s.HEIGHT))
        for y in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (0, y), (s.WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y): # handles any text popups on screen.
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    if not self.paused:
                        self.show_go_screen()
                        self.paused = True
                    else:
                        self.paused = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_w:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_s:
            #         self.player.move(dy=1)

    def show_start_screen(self): #startup screen function
        self.screen.fill(s.BGCOLOR)
        self.draw_text(self.screen, "Collect all coins and avoid the bouncing enemies to win. Press P to pause at any time.", 24, s.WHITE, 5, 8)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, s.WHITE, 10, 10)
        pg.display.flip()
        self.start_screen_events()

    def show_go_screen(self): #pause screen function
        if not self.running:
            return
        # self.screen.fill(s.BGCOLOR)
        self.draw_text(self.screen, "Collect all coins and avoid the bouncing enemies to win.", 24, s.WHITE, 10, 8)
        self.draw_text(self.screen, "Game paused. Please press P to continue.", 24, s.WHITE, 10, 10)
        pg.display.flip()
        self.pause_screen_events()

    def show_end_screen(self): #win screen function
        self.screen.fill(s.BGCOLOR)
        self.draw_text(self.screen, "You have collected all coins! Thanks for playing! Please close the game window.", 24, s.WHITE, 5, 10)
        pg.display.flip()
        self.win_screen_events()

    def show_death_screen(self): #end screen
        self.screen.fill(s.BGCOLOR)
        self.draw_text(self.screen, "You have died. Please close the game window.", 24, s.WHITE, 5, 10)
        pg.display.flip()
        self.dead_screen_events()

    def start_screen_events(self): # conditions for startup screen
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def pause_screen_events(self): # events for pause screen
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        self.paused = False
                        waiting = False

    def win_screen_events(self): # events for win screen
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            self.paused = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
     
    def dead_screen_events(self):  # events for death screen
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                # if event.type == pg.KEYUP:
                #     if event.key == pg.K_r:
                #         self.paused = False
                #         waiting = False
                #         for s in self.all_sprites:
                #             s.kill()
                #         g.new()
                #         g.run()


g = Game()
g.show_start_screen()
while True:
        g.new()
        g.run()
        # g.show_go_screen()
