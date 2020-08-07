import sys

import Renderer
import PathFinders
import pygame

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((Renderer.x_max, Renderer.y_max))
searchers = PathFinders.gensearchers(PathFinders.population)

while True:
    Renderer.rendergrid(Renderer.box_width, Renderer.box_height, window)
    Renderer.renderstartend(window, Renderer.green, Renderer.red)
    pos = pygame.mouse.get_pos()
    pressedl, pressedm, pressedr = pygame.mouse.get_pressed()

    if pressedl:
        Renderer.fillrect(pos, Renderer.blue, window)
        #Renderer.out2dmatrix(Renderer.gridmap)
    if pressedr:
        break

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

while True:
    pygame.display.update()
    Renderer.hidePathFinders(window, searchers, PathFinders.population)
    check = PathFinders.moveallsearchers(searchers, PathFinders.population)
    Renderer.renderPathFinders(window, searchers, PathFinders.population)
    clock.tick(100)

    if check:
        break

    allmovesmade = 1
    for i in range(PathFinders.population):
        if searchers[i].movesmade < PathFinders.lifespan:
            allmovesmade = 0

    if allmovesmade == 1:
        #PathFinders.generation_num += 1
        pool = PathFinders.evaluatesearchers(searchers)
        Renderer.hidePathFinders(window, searchers, PathFinders.population)
        searchers = PathFinders.makechildren(pool)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
