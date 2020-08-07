import math
import random

import Renderer

# Constants
# Species_count = 1
population = 0
lifespan = 0
mutation_percentage = 0  # initial percentage of children that get mutations
generation_num = 0
# bestsearcherindex = 0


# mutation_increase_rate = 15  #generations to increase mutation rate

# Searcher class for the genetic algorithm, stores DNA/genes, fitness level, mutations, etc
class Searcher:
    # variables for each individual searcher
    movesmade = 0
    dna = []
    fitness = 0
    randmoves = 1
    count = 0
    mutata = False

    # __init__(self, x, y, dna, mutate) is the constructor for the Searcher class
    def __init__(self, x, y, dna, mutate):
        self.x = x
        self.y = y
        self.mutate = mutate
        if dna is not None:
            self.dna = dna
            self.randmoves = 0
        else:
            self.randmoves = 1

    # moveright(self) moves the searcher to the right
    def moveright(self):
        self.x += 1
        self.dna.append(0)
        self.movesmade += 1

    # moveleft(self) moves the searcher to the left
    def moveleft(self):
        self.x -= 1
        self.dna.append(1)
        self.movesmade += 1

    # moveup(self) moves the searcher up
    def moveup(self):
        self.y -= 1
        self.dna.append(2)
        self.movesmade += 1

    # movedown(self) moves the searcher down
    def movedown(self):
        self.y += 1
        self.dna.append(3)
        self.movesmade += 1

    # calcfitness(self) calculates the fitness of the searcher
    def calcfitness(self):
        self.fitness = 1 / math.pow(distance((self.x, self.y), (Renderer.grid_width, Renderer.grid_height)), 2)


# distance (pos1, pos2) computes and returns the distance between positions 1 and 2
def distance(pos1, pos2):
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


# movesearcher(searcher, num) takes a number from (0 - 3) and moves the searcher in a specific direction 1 unit
# based on the number
# requires: 0 <= num <= 3
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
            elif num == 3 and searcher.y < Renderer.grid_height - 1 and \
                    Renderer.gridmap[searcher.y + 1][searcher.x] != 1:
                searcher.movedown()
                break
            else:
                num = random.randint(0, 3)


# moveallsearchers(searchers, count) moves all the searchers, count is the length of searchers (ie. population size)
# returns True if a searcher reached the end and false otherwise
def moveallsearchers(searchers, count):
    reachedend = False

    for i in range(count):
        if searchers[i].x == Renderer.grid_width - 1 and searchers[i].y == Renderer.grid_height - 1:
            reachedend = True
            break
        if searchers[i].randmoves == 1 or (searchers[i].mutate and searchers[i].count > (4 * lifespan) / 6):
            movesearcher(searchers[i], random.randint(0, 3))
        else:
            movesearcher(searchers[i], searchers[i].dna[searchers[i].count])
            searchers[i].count += 1

    return reachedend


# gensearchers(count) generates count number of searchers and returns a array of the searchers
def gensearchers(count):
    searchers = [Searcher(Renderer.start_x, Renderer.start_y, None, False) for i in range(count)]
    return searchers


# evaluatesearchers(searchers) evaluates all searchers fitness and generates a childpool where searchers with a
# higher fitness have a higher frequency, returns childpool
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
        for j in range(prob):
            childpool.append(searchers[i])

    return childpool


# crossover(firstparent, secondparent) takes in two "Parent" searchers and crosses their DNA at a random point to
# produce a child searcher's DNA. Returns the Child Searcher's DNA
def crossover(firstparent, secondparent):
    crosspoint = math.floor(random.randint(0, lifespan))
    childdna = []

    for i in range(lifespan):
        if i < crosspoint:
            childdna.append(firstparent.dna[i])
        else:
            childdna.append(secondparent.dna[i])

    return childdna


# makechildren(pool) intakes a pool of potential parents and generates the next generation of searchers based off,
# the parents DNA. Sets a determined percentage of the children to mutate (based on mutation_percentage from user)
# returns the next generation of searchers
def makechildren(pool):
    nextgen = []
    mutation_num = math.floor((mutation_percentage / 100) * population)

    for i in range(mutation_num):
        firstparent = random.choice(pool)
        secondparent = random.choice(pool)
        child = Searcher(Renderer.start_x, Renderer.start_y, crossover(firstparent, secondparent), True)
        nextgen.append(child)

    for i in range(population - mutation_num):
        firstparent = random.choice(pool)
        secondparent = random.choice(pool)
        child = Searcher(Renderer.start_x, Renderer.start_y, crossover(firstparent, secondparent), False)
        nextgen.append(child)

    return nextgen
