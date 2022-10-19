import pygame
from pygame.draw import *


FPS = 60

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (128,128,128)
BROWN = (139,69,19)


screen = pygame.display.set_mode((900, 900), pygame.NOFRAME)


pygame.init()
screen.fill((11, 16, 61))
ghost = pygame.image.load('/ghost3.png')


def coord_handler(coords:list, handle:int) -> list:
    new_coords = []
    for x,y in coords:
        new_coords.append((x+handle, y+handle))
    return new_coords

def draw_tower():
    screen.fill([11, 16, 61, 0])
    polygon(screen, GRAY, coord_handler([(200,100),(350,200),(300,300),(300,600),(100,600),(100,300),(50,200)], 100))
    rect(screen,BLACK, (250,550,100,600))
    rect(screen,BROWN, (0,700,900,900))


def draw_ghost(x,y):
    surface1 = ghost.convert_alpha()
    screen.blit(surface1, (x, y))


clock = pygame.time.Clock()

ghost_coords = [350,300]
is_mouse_move = False
while True:
    clock.tick(FPS)

    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        ghost_coords[0] += 10
    if key[pygame.K_a]:
        ghost_coords[0] -= 10
    if key[pygame.K_w]:
        ghost_coords[1] -= 10
    if key[pygame.K_s]:
        ghost_coords[1] += 10

    if ghost_coords[0] > 850:
        ghost_coords[0] = -200
    elif ghost_coords[0] < -350:
        ghost_coords[0] = 800

    if ghost_coords[1] < -380:
        ghost_coords[1] = 800
    elif ghost_coords[1] > 850:
        ghost_coords[1] = -300

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEMOTION and is_mouse_move:
                ghost_coords = [event.pos[0]-150,event.pos[1]-150]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_mouse_move = not is_mouse_move
            ghost_coords = [event.pos[0] - 150, event.pos[1] - 150]

            print(event)
    else:
        draw_tower()
        draw_ghost(ghost_coords[0], ghost_coords[1])
        pygame.display.update()
        continue
    break
pygame.quit()

