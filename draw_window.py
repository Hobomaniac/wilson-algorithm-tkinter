from tkinter import *
from tkinter import ttk

from maze import *

def create_grid(maze: Maze) -> list:
    grid_size = (maze.size * 2) + 1

    grid = []

    for y in range(grid_size):
        grid.append([])
        for x in range(grid_size):
            grid[y].append(Cell.WALL)
    return grid

def set_default_walls(grid:list) -> None:
    for y in range(len(grid)):
        for x in range(len(grid[y])):

            if x == 0 or x == len(grid[y])-1:
                grid[y][x] = Cell.WALL 
            elif y == 0 or y == len(grid)-1:
                grid[y][x] = Cell.WALL
            elif y % 2 == 0 and x % 2 == 0:
                grid[y][x] = Cell.WALL


def update_walls(grid: list, maze: Maze) -> None:
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):

            cx = int((x-1) / 2)
            cy = int((y-1) / 2)

            if y % 2 == 1 and x % 2 == 1:
                grid[y][x] = maze.cells[cy][cx].type
            elif x % 2 == 1 and y % 2 == 0:
                grid[y][x] = maze.cells[cy][cx].connections['E']
            elif y % 2 == 1 and x % 2 == 0:
                grid[y][x] = maze.cells[cy][cx].connections['S']

def draw_grid(canvas: Canvas, grid: list, cell_length: int) -> None:

    for y in range(len(grid)):
        for x in range(len(grid[y])):

            x1 = x * cell_length
            y1 = y * cell_length
            x2 = x * cell_length + cell_length
            y2 = y * cell_length + cell_length
            
            c_type = grid[y][x]
            match c_type:
                case Cell.FLOOR:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="grey")
                case Cell.WALL:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="blue")
                case Cell.TEMP:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")
                case Cell.POINT:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="green")

def show_grid_console(grid: list) -> None:
    for row in grid:
        print(row)
    print()

def update(canvas: Canvas, state:str, grid:list,  maze: Maze, cell_length: int, counter: int) -> str:
    canvas.delete("all")

    state = generate_maze(state, maze, counter)

    #update_walls(grid, maze)
    grid = set_grid(maze)
    draw_grid(canvas, grid, cell_length)

    canvas.after(1, update, canvas, state, grid, maze, cell_length, counter)

def main() -> None:
    cell_length = 20
    my_maze = create_maze(20)

    state = 'Init'
    _counter = 0 

    my_grid = set_grid(my_maze)
    grid_size = len(my_grid) * cell_length

    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    canvas = Canvas(root, width=grid_size, height=grid_size, background='gray75')
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))

    canvas.after(500, update, canvas, state, my_grid, my_maze, cell_length, _counter)

    root.mainloop()

if __name__ == "__main__":
    #main()
    cell_length = 3 

    my_maze = create_maze(100)

    state = 'Init'
    _counter = 0 

    while state != 'Finished':
        state = generate_maze(state, my_maze, _counter)
    print("Finished generating maze")

    my_grid = set_grid(my_maze)
    grid_size = len(my_grid) * cell_length

    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    canvas = Canvas(root, width=grid_size, height=grid_size, background='gray75')

    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    
    draw_grid(canvas, my_grid, cell_length)

    #set_default_walls(my_grid)
    #canvas.after(500, update, canvas, "Init", my_grid, my_maze, cell_length)

    root.mainloop()



