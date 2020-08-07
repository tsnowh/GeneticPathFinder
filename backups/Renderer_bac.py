import pygame
import PathFinders

# Constants
y_max = 600
y_min = 0
x_max = 600
x_min = 0
box_width = 20
box_height = 20
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
searcher_color = (255, 0, 0)
start_x = 0
start_y = 0
grid_width = y_max // box_width
grid_height = x_max // box_width

rows, cols = ((x_max // box_width), (y_max // box_width))
gridmap = [[0 for i in range(cols)] for j in range(rows)]


def out2dmatrix(matrix):
    for row in matrix:
        print(row)
    print()


def rendergrid(width, height, window):
    for j in range((y_max // width) + 1):
        for i in range((x_max // width) + 1):
            pygame.draw.rect(window, white, (x_min, y_min, x_min + (width * i), y_min + (height * j)), 1)


def fillrect(pos, color, window):
    x = (pos[0] // box_width) * box_width
    y = (pos[1] // box_height) * box_height

    pygame.draw.rect(window, color, (x, y, box_width, box_height))
    gridmap[(pos[1] // box_height)][(pos[0] // box_width)] = 1
    # print((pos[0] // box_width), (pos[1] // box_height))


def renderstartend(window, s_color, e_color):
    pygame.draw.rect(window, s_color, (x_min, y_min, x_min + box_width, y_min + box_height))
    pygame.draw.rect(window, e_color, (x_max - box_width, y_max - box_height, box_width, box_height))

def renderPathFinders(window, searchers, count):
    for i in range(count):
        pygame.draw.rect(window, searcher_color,
                         ((searchers[i].x * box_width) + box_width // 2 - 4,
                          (searchers[i].y * box_height) + box_height // 2 - 4, 8, 8))

def hidePathFinders(window, searchers, count):
    pygame.draw.rect(window, green, (box_width // 2 - 4, box_height // 2 - 4, 8, 8))
    for i in range(count):
        pygame.draw.rect(window, black,
                         ((searchers[i].x * box_width) + box_width // 2 - 4,
                          (searchers[i].y * box_height) + box_height // 2 - 4, 8, 8))
