import pygame as pg
FPS = 30
clock = pg.time.Clock()

frames = ["frame 1","frame 2","frame 3","frame 4"]
current_frame = 0
frames_length = len(frames)
then = 0
while True: 
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 1000:
        print(now)
        then = now
        print(frames[current_frame%frames_length])
        current_frame += 1