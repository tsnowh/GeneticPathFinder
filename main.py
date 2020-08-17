import sys

import Renderer
import PathFinders
import pygame

# initializes pygame
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((Renderer.x_max, Renderer.y_max))

# main loop for program
while True:
    pygame.display.update()

    # initializes and runs the interface
    interface = Renderer.Interface()
    interface.runinterface()

    # print(PathFinders.population) # debugging
    # print(PathFinders.lifespan) # debugging
    # print(PathFinders.mutation_percentage) # debugging

    # generates new bath of searchers
    searchers = PathFinders.gensearchers(PathFinders.population)

    # loop for user to create blockades
    while True:
        Renderer.rendergrid(Renderer.box_width, Renderer.box_height, window)
        Renderer.renderstartend(window, Renderer.green, Renderer.red)

        pos = pygame.mouse.get_pos()
        pressedl, pressedm, pressedr = pygame.mouse.get_pressed()

        # if left mouse button clicked it creates blockade at the position of click
        if pressedl:
            Renderer.fillrect(pos, Renderer.blue, window)
            Renderer.gridmap[(pos[1] // Renderer.box_height)][(pos[0] // Renderer.box_width)] = 1
            # Renderer.out2dmatrix(Renderer.gridmap) # debugging
        if pressedr:
            break

        # checks for user input to close game or mouse clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # print(pos)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update pygame display
        pygame.display.update()

    # loop for genetic algorithm
    while True:
        # updates display
        pygame.display.update()

        # controls searchers
        Renderer.hidePathFinders(window, searchers, PathFinders.population)
        check = PathFinders.moveallsearchers(searchers, PathFinders.population, window)
        Renderer.renderPathFinders(window, searchers, PathFinders.population)

        # sets frame rate / delay
        clock.tick(100)

        # breaks loop if end is reached
        if check:
            break

        # checks if all searchers reached their lifespan
        allmovesmade = 1
        for i in range(PathFinders.population):
            if searchers[i].movesmade < PathFinders.lifespan:
                allmovesmade = 0

        # if all searchers reached their lifespan then next generation of searchers is generated
        if allmovesmade == 1:
            PathFinders.lifespan += 40
            PathFinders.generation_num += 1
            pool = PathFinders.evaluatesearchers(searchers)
            Renderer.hidePathFinders(window, searchers, PathFinders.population)
            searchers = PathFinders.makechildren(pool)

        # checks for user input (window is closed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

    # loop to break after searchers reached end
    while True:
        pygame.display.update()
        event = pygame.event.wait()

        # if any key is pressed breaks loop
        if event.type == pygame.KEYDOWN:
            break

    # resets window for next iteration
    window.fill(Renderer.black)
    Renderer.gridmap = [[0 for i in range(Renderer.cols)] for j in range(Renderer.rows)]

    # checks if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break
