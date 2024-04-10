# THis file was created by: Robbie Raiche.

# I'm finna create a player class and a wall class

# Import stuff
import pygame as pg
from pygame.sprite import Sprite
import settings as s


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
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
        # self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE

    # def move(self, dx=0, dy=0,):
    #     self.x += dx
    #     self.y += dy
    
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
        self.image = pg.Surface((s.TILESIZE,s.TILESIZE))
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
        self.image = pg.Surface((s.TILESIZE, s.TILESIZE))
        self.image.fill(s.LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x * s.TILESIZE
        self.y = y * s.TILESIZE
        self.rect.x = x
        self.rect.y = y
        self.vx = s.ENEMY_SPEED
        self.vy = s.ENEMY_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071               # MATH!!
            self.vy *= 0.7071

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

