from tkinter import *
from main import *
from tkinter import messagebox
import numpy as np
class Cell():
    BlOCKED_COLOR_BG = "green"
    TARGET_COLOR_BG = "blue"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "black"
    START_COLOR_BG = "black"
    def __init__(self, master, x, y, size,colour):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= colour
        self.xmin = self.abs * self.size
        self.xmax = self.xmin + self.size
        self.ymin = self.ord * self.size
        self.ymax = self.ymin + self.size
        self.a,self.b=(self.xmin+self.xmax)/2,(self.ymin+self.ymax)/2
    def _switch(self,t):
        """ Switch if the cell is filled or not. """
        self.fill= t

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :

            if self.fill==0:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if self.fill==1:
                fill = Cell.BlOCKED_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if self.fill==2:
                fill = Cell.TARGET_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if self.fill==3:
                fill = Cell.START_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            self.master.create_rectangle(self.xmin, self.ymin, self.xmax, self.ymax, fill = fill, outline = outline)

    def drawArrow(self,type):
        if type==0:
            self.master.create_line(self.a, self.ymin, self.a, self.ymax, arrow= FIRST)
        if type==1:
            self.master.create_line(self.xmax, self.ymin, self.xmin, self.ymax, arrow= FIRST)
        if type==2:
            self.master.create_line(self.xmin, self.b, self.xmax, self.b, arrow= LAST)
        if type==3:
            self.master.create_line(self.xmin, self.ymin, self.xmax, self.ymax, arrow= LAST)
        if type==4:
            self.master.create_line(self.a, self.ymin, self.a, self.ymax, arrow= LAST)
        if type==5:
            self.master.create_line(self.xmax, self.ymin, self.xmin, self.ymax, arrow= LAST)
        if type==6:
            self.master.create_line(self.xmin, self.b, self.xmax, self.b, arrow= FIRST)
        if type==7:
            self.master.create_line(self.xmin, self.ymin, self.xmax, self.ymax, arrow= FIRST)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber + 230, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize,0))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.blocked = []
        self.end = []
        self.start = []
        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        #self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch(para)
        cell.draw()
        if para==1:
            self.blocked.append(cell)
        if para==2:
            self.start.append(cell)
        if para==3:
            self.end.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.blocked or cell not in self.start or cell not in self.end:
            cell._switch(para)
            cell.draw()
            if para==1:
                self.blocked.append(cell)
            if para==2:
                self.start.append(cell)
            if para==3:
                self.end.append(cell)
def generateobs():
    global para,obs
    obs=set([( i.ord,i.abs) for i in grid.blocked ])
    para=2


def generateStart():
    global para,start
    start=[( i.ord,i.abs) for i in grid.start ]
    para=3

def generatetargets():

    end=[( i.ord,i.abs) for i in grid.end ]
    #print(start,end,obs)

    Map= np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            if (i,j) in obs:
                Map[i,j]=1

    route = aStar(Map,start[0],end[0],x,y)
    route.append(start[0])
    route=route[::-1]
    #print(route)
    if len(route)!=1:
        buildPath(route)
    else:
        messagebox.showinfo("!!!!", "No path found")
def buildPath(route):
    neighbors = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    for i in range(len(route)-1):
        p,q=route[i]
        P,Q=route[i+1]
        j,k=P-p,Q-q
        for l in range(8):
            if (j,k)==neighbors[l]:
                grid.grid[p][q].drawArrow(l)
def initialize():
    app = Tk()
    global grid,para
    para=1
    grid = CellGrid(app, x, y, 60)

    label = Label(grid, text= '1 . Mark the obstacles ' ,font=('helvetica', 10))
    grid.create_window(y*60/2, x*60+20, window=label)

    button2 = Button(grid,text='Obstacles marked', command=generateobs, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    grid.create_window(y*60/2, x*60+50, window=button2)

    label1 = Label(grid, text= '2 . Mark the start point ' ,font=('helvetica', 10))
    grid.create_window(y*60/2, x*60+80, window=label1)

    button3 = Button(grid,text='Start point marked', command=generateStart, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    grid.create_window(y*60/2, x*60+110, window=button3)

    label2 = Label(grid, text= '3 . Mark the end point ' ,font=('helvetica', 10))
    grid.create_window(y*60/2, x*60+140, window=label2)

    button4 = Button(grid,text='End point marked', command=generateStart, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    grid.create_window(y*60/2, x*60+170, window=button4)

    button4 = Button(grid,text='Calculate optimal path', command=generatetargets, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    grid.create_window(y*60/2, x*60+200, window=button4)

    grid.pack()
    app.mainloop()

def getSquareRoot ():
    global x,y
    x = int(entry1.get())
    y = int(entry2.get())
    initialize()


root= Tk()
canvas1 = Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()
label2 = Label(root, text='Enter height:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 50, window=label2)
entry1 = Entry (root)
canvas1.create_window(200, 75, window=entry1)
label3 = Label(root, text='Enter width:')
label3.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label3)
entry2 = Entry (root)
canvas1.create_window(200, 125, window=entry2)
button1 = Button(text='Build grid', command=getSquareRoot, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()
