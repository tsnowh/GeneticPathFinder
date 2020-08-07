import math
import random

import Renderer

population = 100
lifespan = 100
# mutation_chance = 5  # initial percentage of children that get mutations
generation_num = 0


# mutation_increase_rate = 15  #generations to increase mutation rate


class Searcher:
    movesmade = 0
    dna = []
    fitness = 0
    randmoves = 1
    count = 0

    def __init__(self, x, y, dna):
        self.x = x
        self.y = y
        if dna is not None:
            self.dna = dna
            self.randmoves = 0
        else:
            self.randmoves = 1

    def moveright(self):
        self.x += 1
        self.dna.append(0)
        self.movesmade += 1

    def moveleft(self):
        self.x -= 1
        self.dna.append(1)
        self.movesmade += 1

    def moveup(self):
        self.y -= 1
        self.dna.append(2)
        self.movesmade += 1

    def movedown(self):
        self.y += 1
        self.dna.append(3)
        self.movesmade += 1

    def calcfitness(self):
        self.fitness = 1 / math.pow(distance((self.x, self.y), (Renderer.grid_width, Renderer.grid_height)), 2)


def distance(pos1, pos2):
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


def movesearcher(searcher, num):
    while True:
        if searcher.movesmade < lifespan:
            if num == 0 and searcher.x < Renderer.grid_width - 1 and Renderer.gridmap[searcher.y][searcher.x + 1] != 1:
                searcher.moveright()
                break
            elif num == 1 and searcher.x > Renderer.start_x and Renderer.gridmap[searcher.y][searcher.x - 1] != 1:
                searcher.moveleft()
                break
            elif num == 2 and searcher.y > Renderer.start_y and Renderer.gridmap[searcher.y - 1][searcher.x] != 1:
                searcher.moveup()
                break
            elif num == 3 and searcher.y < Renderer.grid_height - 1 and Renderer.gridmap[searcher.y + 1][searcher.x] != 1:
                searcher.movedown()
                break
            else:
                num = random.randint(0, 3)


def moveallsearchers(searchers, count):
    reachedend = False

    for i in range(count):
        if searchers[i].x == Renderer.grid_width - 1 and searchers[i].y == Renderer.grid_height - 1:
            reachedend = True
            break
        if searchers[i].randmoves == 1:
            movesearcher(searchers[i], random.randint(0, 3))
        else:
            movesearcher(searchers[i], searchers[i].dna[searchers[i].count])
            searchers[i].count += 1

    return reachedend


def gensearchers(count):
    searchers = [Searcher(Renderer.start_x, Renderer.start_y, None) for i in range(count)]
    return searchers


def evaluatesearchers(searchers):
    maxfitness = 0
    for i in range(population):
        searchers[i].calcfitness()
        if searchers[i].fitness > maxfitness:
            maxfitness = searchers[i].fitness

    for i in range(population):
        searchers[i].fitness /= maxfitness

    childpool = []
    for i in range(population):
        prob = math.floor(searchers[i].fitness * 100)
        #print(prob)
        for j in range(prob):
            childpool.append(searchers[i])

    return childpool


def crossover(firstparent, secondparent):
    crosspoint = math.floor(random.randint(0, lifespan))
    childdna = []

    for i in range(lifespan):
        if i < crosspoint:
            childdna.append(firstparent.dna[i])
        else:
            childdna.append(secondparent.dna[i])

    return childdna


def makechildren(pool):
    nextgen = []

    for i in range(population):
        firstparent = random.choice(pool)
        secondparent = random.choice(pool)
        child = Searcher(Renderer.start_x, Renderer.start_y, crossover(firstparent, secondparent))
        nextgen.append(child)

    return nextgen
