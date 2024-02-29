# This file was created by Robbie Raiche

# My first source control edit!!1!!1!!
# Import stuff
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path

# Creating the game class
class Game:
    # initialize 
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    # load save game data etc
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        
    def new(self):
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
                print(col)
                # print(tile)
                if tile == '1':
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self,col,row)
                if tile == "C":
                    Coin(self,col,row)
                if tile == "E":
                    Enemy(self,col,row)
            
 # define the run method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self): # x button works now
        pg.quit()
        sys.exit()

    def update(self): # UPDATE EVERYTHING!!
        self.all_sprites.update()

    def draw_grid(self): # draw the grid with the tile size from settings
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self): # draw the background and the grid and all the sprites
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "COIN: " + str(self.player.coin), 64, YELLOW, 1, 1)
        self.draw_text(self.screen, "HP: " + str(self.player.hp), 64, LIGHTGREY, 1, 3)
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
