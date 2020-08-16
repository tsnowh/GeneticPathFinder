import pygame

import PathFinders
import tkinter

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
gridmap = [[0 for i in range(cols)] for j in range(rows)]  # matrix to keep track of blockades


# interface class for choosing intial conditions for the genetic algorithm
class Interface:
    root = tkinter.Tk()

    # setpop(self, val) sets the population variable (from PathFinders) for the genetic algorithm to val
    def setpop(self, val):
        PathFinders.population = int(val)

    # setlife(self, val) sets the lifespan variable (from PathFinders) for the genetic algorithm to val
    def setlife(self, val):
        PathFinders.lifespan = int(val)

    # setmut(self, val) sets the mutation_percentage variable (from PathFinders) for the genetic algorithm to val
    def setmut(self, val):
        PathFinders.mutation_percentage = int(val)

    # startbutton(self) is a command for the startbutton which hides the interface display and starts the genetic
    # algorithm setup in the pygame window
    def startbutton(self):
        # self.root.destory()
        self.root.withdraw()
        self.root.quit()

    # resetwindow(self, topframe, midframe1, midframe2, botframe) resets the interface window by freeing the
    # widgets in each of the four frames then frees the frames
    def resetwindow(self, topframe, midframe1, midframe2, botframe):
        for widget in topframe.winfo_children():
            widget.destroy()

        topframe.pack_forget()

        for widget in midframe1.winfo_children():
            widget.destroy()

        midframe1.pack_forget()

        for widget in midframe2.winfo_children():
            widget.destroy()

        midframe2.pack_forget()

        for widget in botframe.winfo_children():
            widget.destroy()

        botframe.pack_forget()

    # runinterface(self) is the main function for the interface which initialises the frames and widgets and displays
    # them onto the window
    def runinterface(self):
        self.root.update()
        self.root.deiconify()
        self.root.geometry('600x300')
        self.root.title("PathFinderMenu")
        topframe = tkinter.Frame(self.root)
        # topframe.grid()
        midframe1 = tkinter.Frame(self.root)
        midframe2 = tkinter.Frame(self.root)
        botframe = tkinter.Frame(self.root)

        topframe.pack(pady=10)
        midframe1.pack(pady=10)
        midframe2.pack(pady=10)
        botframe.pack()

        instructionstop = tkinter.Text(topframe, height=2, width=35)
        instructionstop.insert(tkinter.END, "left click on boxes to turn\nthem into a blue blockade")

        instructionsmid = tkinter.Text(midframe1, height=2, width=35)
        instructionsmid.insert(tkinter.END, "once all blockades are created\nright click to begin algorithm")

        instructionsmid2 = tkinter.Text(midframe2, height=2, width=35)
        instructionsmid2.insert(tkinter.END, "after path has been found press\nany key to restart program")

        popslider = tkinter.Scale(topframe, from_=0, to=1000, resolution=1, orient=tkinter.HORIZONTAL,
                                  command=lambda val: self.setpop(val))
        lifeslider = tkinter.Scale(midframe1, from_=0, to=500, resolution=1, orient=tkinter.HORIZONTAL,
                                   command=lambda val: self.setlife(val))
        mutslider = tkinter.Scale(midframe2, from_=0, to=100, resolution=1, orient=tkinter.HORIZONTAL,
                                  command=lambda val: self.setmut(val))

        poplabel = tkinter.Label(topframe, text="Initial Population Size:")
        lifelabel = tkinter.Label(midframe1, text="Initial Lifespan:")
        mutlabel = tkinter.Label(midframe2, text="Mutation Change (%):")
        start = tkinter.Button(botframe, text="Start PathFinder",
                               command=self.startbutton)

        instructionstop.pack(side=tkinter.LEFT)
        poplabel.pack(padx=10, side=tkinter.LEFT)
        popslider.pack(side=tkinter.LEFT)
        instructionsmid.pack(side=tkinter.LEFT)
        lifelabel.pack(padx=30, side=tkinter.LEFT)
        lifeslider.pack(side=tkinter.LEFT)
        instructionsmid2.pack(side=tkinter.LEFT)
        mutlabel.pack(padx=10, side=tkinter.LEFT)
        mutslider.pack(side=tkinter.LEFT)
        start.pack()

        self.root.mainloop()

        self.resetwindow(topframe, midframe1, midframe2, botframe)


# out2dmatrix(matrix) takes in a two dimensional matrix and outputs it to the console
# used for debugging (not called in finished program)
# usually used in conjunction with the gridmap variable
def out2dmatrix(matrix):
    for row in matrix:
        print(row)
    print()


# rendergrid(width, height, window) renders the main grid for the application in the pygame window with the
# dimensions passed into it (width x height)
def rendergrid(width, height, window):
    for j in range((y_max // width) + 1):
        for i in range((x_max // width) + 1):
            pygame.draw.rect(window, white, (x_min, y_min, x_min + (width * i), y_min + (height * j)), 1)


# fillrect(pos, color, window) fills in the rectangles in the grid which contains the position pos
def fillrect(pos, color, window):
    x = (pos[0] // box_width) * box_width
    y = (pos[1] // box_height) * box_height

    pygame.draw.rect(window, color, (x, y, box_width, box_height))
    gridmap[(pos[1] // box_height)][(pos[0] // box_width)] = 1
    # print((pos[0] // box_width), (pos[1] // box_height))


# renderstartend(window, s_color, e_color) renders the start and the end locations on the grid
# start in green, end in red
def renderstartend(window, s_color, e_color):
    pygame.draw.rect(window, s_color, (x_min, y_min, x_min + box_width, y_min + box_height))
    pygame.draw.rect(window, e_color, (x_max - box_width, y_max - box_height, box_width, box_height))


# renderPathFinders(window, searchers, count) renders the pathfinders used in the genetic algorithm,
# searchers is an array of pathfinders and count is the array length (ie. population size)
def renderPathFinders(window, searchers, count):
    for i in range(count):
        pygame.draw.rect(window, searcher_color,
                         ((searchers[i].x * box_width) + box_width // 2 - 4,
                          (searchers[i].y * box_height) + box_height // 2 - 4, 8, 8))


# hidePathFinders(window, searchers, count) hides all pathfinders in the array searchers, with length count
# (population size)
def hidePathFinders(window, searchers, count):
    pygame.draw.rect(window, green, (box_width // 2 - 4, box_height // 2 - 4, 8, 8))
    for i in range(count):
        pygame.draw.rect(window, black,
                         ((searchers[i].x * box_width) + box_width // 2 - 4,
                          (searchers[i].y * box_height) + box_height // 2 - 4, 8, 8))
