# THis file was created by: Robbie Raiche.

# I'm finna create a player class and a wall class

# Import stuff
import pygame as pg
from pygame.sprite import Sprite
import settings as s
from os import path

SPRITESHEET = "theBell.png" # This is the path to the spritesheet image file. It's in the images folder.
ENEMYSHEET = "roombaSpritesheet.png"
CHAIRSHEET = "office-chair.png"

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        
        if self.filename == path.join(img_folder, SPRITESHEET):
            image = pg.transform.scale(image, (width * 2, height * 2)) # Control the multipliers to multiply size
        return image
    
# Capitalize the class name. It's the LAW!!
class Player(Sprite):
# This makes the player class a subclass of Sprite, imported from Pygame. Now the player class can do everything that Sprite module class thing can do.
    def __init__(self,game,x,y): 
        self.groups = game.all_sprites, game.collision
        Sprite.__init__(self, self.groups)
        self.game = game
        self.hp = 3
        self.coin = 0
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE
        self.current_frame = 0
        self.last_update = 0

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32).convert_alpha(), 
                                self.spritesheet.get_image(32,0, 32, 32).convert_alpha()]
        for frame in self.standing_frames:
            frame.set_colorkey((255, 255, 255))  # Set the colorkey to white screen(copilot)
        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -s.PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = s.PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -s.PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = s.PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071               # MATH!!
            self.vy *= 0.7071
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx <0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.width
                if self.vy <0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
            
    def collide_with_obj(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.coin += 1
            if str(hits[0].__class__.__name__) == "Enemy":
                self.hp -= 1
                s.loaded_enemies -= 1
                print(s.loaded_enemies)
            if str(hits[0].__class__.__name__) == "Elevator":
                s.inelevator = True
                
           
    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
       self.get_keys()
       self.animate()
       self.x += self.vx * self.game.dt
       self.y += self.vy * self.game.dt
       self.rect.x = self.x
       self.collide_with_walls('x')
       self.rect.y = self.y
       self.collide_with_walls('y')
       self.collide_with_obj(self.game.coins, True)
       self.collide_with_obj(self.game.enemies, True)
       self.collide_with_obj(self.game.elevators, True)


class Wall(Sprite):
    def __init__(self, game, x, y): 
        self.groups = game.all_sprites, game.walls, game.collision
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((s.TILESIZE, s.TILESIZE))
        self.image.fill(s.WALLCOLOR)
        self.rect = self.image.get_rect()
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE 
        self.rect.x = x * s.TILESIZE
        self.rect.y = y * s.TILESIZE

class Coin(Sprite): # dis a copy of the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((s.TILESIZE, s.TILESIZE))
        self.image.fill(s.COINCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * s.TILESIZE
        self.rect.y = y * s.TILESIZE

class Enemy(Sprite): # dis a copy of the other class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        # Load the image file for the enemy
        self.spritesheet = Spritesheet(path.join(img_folder, ENEMYSHEET))
        self.load_images()
        self.image = self.standing_frames[0]  # Set self.image to the first standing frame
        self.rect = self.image.get_rect()
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE
        self.vx = s.ENEMY_SPEED
        self.vy = s.ENEMY_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071               # MATH!!
            self.vy *= 0.7071
        
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32).convert_alpha(), 
                                self.spritesheet.get_image(32,0, 32, 32).convert_alpha(),
                                self.spritesheet.get_image(64,0, 32, 32).convert_alpha(),
                                self.spritesheet.get_image(96,0, 32, 32).convert_alpha()]
        for frame in self.standing_frames:
            frame.set_colorkey((35, 214, 34))  # Set the colorkey to green screen(copilot)
        
    def animate(self):
        if self.vx > 0 and self.vy < 0:
            self.image = self.standing_frames[0]
        elif self.vx < 0 and self.vy < 0:
            self.image = self.standing_frames[1]
        elif self.vx < 0 and self.vy > 0:
            self.image = self.standing_frames[2]
        elif self.vx > 0 and self.vy > 0:
            self.image = self.standing_frames[3]

    def collide_with_obj(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False) # self.game.collision includes walls and player for player bounce
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx <0:
                    self.x = hits[0].rect.right
                self.vx = -self.vx
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.width
                if self.vy <0:
                    self.y = hits[0].rect.bottom
                self.vy = -self.vy
                self.rect.y = self.y

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y =  self.y * TILESIZE
       self.x += self.vx * self.game.dt
       self.y += self.vy * self.game.dt
       self.rect.x = self.x
       self.collide_with_obj('x')
       self.rect.y = self.y 
       self.collide_with_obj('y')
       self.animate()

class Elevator(Sprite): # copy of coin class for elevator
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.elevators
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((s.TILESIZE, s.TILESIZE))
        self.image.fill(s.ELEVCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * s.TILESIZE
        self.rect.y = y * s.TILESIZE

class Chair(Sprite):
    def __init__(self, game, x, y, orientation): 
        self.groups = game.all_sprites, game.chairs
        Sprite.__init__(self, self.groups)
        self.orientation = orientation
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_folder, CHAIRSHEET))
        self.load_images()
        self.image_select()
        # self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE 
        self.rect.x = self.x  # Set the x position of self.rect
        self.rect.y = self.y  # Set the y position of self.rect
        
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32).convert_alpha(), 
                                self.spritesheet.get_image(32,0, 32, 32).convert_alpha(),
                                self.spritesheet.get_image(64,0, 32, 32).convert_alpha(),
                                self.spritesheet.get_image(96,0, 32, 32).convert_alpha()]
        for frame in self.standing_frames:
            frame.set_colorkey((255, 255, 255))
        
    def image_select(self):
        if self.orientation == "down":
            self.image = self.standing_frames[0]
        elif self.orientation == "left":
            self.image = self.standing_frames[1]
        elif self.orientation == "up":
            self.image = self.standing_frames[2]
        elif self.orientation == "right":
            self.image = self.standing_frames[3]
