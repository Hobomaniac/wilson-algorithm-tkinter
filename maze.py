import random
import time

class Cell:

    FLOOR = 0
    WALL = 1
    TEMP = 2
    POINT = 3
    
    REVERSE_DIR = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
            }

    def __init__(self, type: int):
        self.type = type
        self.neighbors = {
                'N': None,
                'E': None,
                'S': None,
                'W': None
                } 
        self.connections = {
                'N': Cell.WALL,
                'E': Cell.WALL,
                'S': Cell.WALL, 
                'W': Cell.WALL 
                } 

    def convert_connections(self, cell_type: int) -> list:
        dir_switch = []
        for sym in ['N', 'S', 'E', 'W']:
            if self.connections[sym] == Cell.TEMP:
                self.connections[sym] = cell_type
                dir_switch.append(sym) 

        return dir_switch

class Maze:

    def __init__(self, size: int):
        self.size = size
        self.length_counter = int(self.size * 2) 
        self.counting = 0
        self.picked = [] 
        self.unpicked = []
        self.cells = []

        self.pointer = None
        self.prev = None

def create_maze(maze_size: int) -> Maze:
    
    maze = Maze(maze_size) 

    for y in range(maze_size):

        maze.cells.append([])
        for x in range(maze_size):

            cell = Cell(Cell.WALL) 
            maze.cells[y].append(cell)
            maze.unpicked.append(cell) 

            if x > 0:
                cell.neighbors['W'] = maze.cells[y][x-1]
                maze.cells[y][x-1].neighbors['E'] = cell
            if y > 0:
                cell.neighbors['N'] = maze.cells[y-1][x]
                maze.cells[y-1][x].neighbors['S'] = cell 

    return maze    

def generate_maze(gen_state: str, maze: Maze, counter: int) -> str:

    print(f" Counter: {maze.counting}")
    
    if maze.counting > maze.length_counter and len(maze.picked) < 2:
        gen_state = 'SetPath'
        maze.counting = 0 

    match gen_state:
        case 'Init':
            return pick_start_cell(maze) 
        case 'StartPath':
            return pick_start_path(maze, counter)
        case 'RandomDir':
            return random_dir_move(maze, counter)
        case 'ResetPath':
            return reset_path(maze)
        case 'Finished':
            return 'Finished'
        case 'SetPath':
            maze.counting += 1
            return set_path(maze)



# pick a random maze cell and turn it into a floor cell
def pick_start_cell(maze: Maze) -> str:
    
    randomrow = random.choice(maze.cells)
    randomcell = random.choice(randomrow)

    randomcell.type = Cell.FLOOR
    maze.unpicked.remove(randomcell)
    maze.picked.append(randomcell)

    return "StartPath"

# pick a random maze cell and turn it into a temp cell
def pick_start_path(maze: Maze, counter:int) -> str:

    if len(maze.unpicked) == 0:
        return "Finished"

    randomcell = random.choice(maze.unpicked)
    maze.pointer = randomcell
    maze.pointer.type = Cell.POINT
    maze.counting += 1

    return 'RandomDir'


# from the temp cell, pick a random direction and create another temp cell
def random_dir_move(maze: Maze, counter: int) -> str:

    randomdir = ['N', 'E', 'S', 'W']
    choicedir = random.choice(randomdir) 

    if maze.pointer.neighbors[choicedir] == None:
        return 'RandomDir'

    if maze.pointer.neighbors[choicedir].type == Cell.WALL:

        maze.pointer.type = Cell.TEMP
        maze.pointer.connections[choicedir] = Cell.TEMP
        maze.prev = maze.pointer 

        maze.pointer = maze.pointer.neighbors[choicedir]
        maze.pointer.type = Cell.POINT
        maze.pointer.connections[Cell.REVERSE_DIR[choicedir]] = Cell.TEMP

        maze.counting += 1
        
        return 'RandomDir'

    elif maze.pointer.neighbors[choicedir].type == Cell.FLOOR:

        maze.pointer.connections[choicedir] = Cell.TEMP
        maze.pointer.neighbors[choicedir].connections[Cell.REVERSE_DIR[choicedir]] = Cell.FLOOR
        maze.pointer.type = Cell.TEMP

        for y in range(len(maze.cells)):
            for x in range(len(maze.cells[y])):
                if maze.cells[y][x].type == Cell.TEMP:
                    maze.cells[y][x].type = Cell.FLOOR
                    maze.cells[y][x].convert_connections(Cell.FLOOR)
                    maze.unpicked.remove(maze.cells[y][x])
                    maze.picked.append(maze.cells[y][x])

        maze.counting = 0

        return 'StartPath'

    elif maze.pointer.neighbors[choicedir].type == Cell.TEMP:
        
        dir_switched = maze.pointer.convert_connections(Cell.WALL)
        maze.prev.connections[Cell.REVERSE_DIR[dir_switched[0]]] = Cell.WALL
        maze.pointer.type = Cell.WALL
        maze.pointer = maze.prev
        maze.pointer.type = Cell.POINT
        
        for sym in ['N', 'S', 'E', 'W']:
            if maze.pointer.connections[sym] == Cell.TEMP:
                maze.prev = maze.pointer.neighbors[sym]

        maze.counting -= 1

        return 'RandomDir' 

    else:

        print(f"No cell type of {maze.pointer.neighbors[choicedir].type}")
        return 'RandomDir'

# reset the path if it has not been able to find the maze in time
def reset_path(maze: Maze) -> str:

    for y in range(len(maze.cells)):
        for x in range(len(maze.cells[y])):

            maze.cells[y][x].convert_connections(Cell.WALL)
            maze.cells[y][x].type = Cell.WALL

    maze.pointer = None
    maze.prev = None

    return 'StartPath'

def set_path(maze: Maze) -> str:
    
    picked_cell = maze.picked.pop()
    picked_cell.type = Cell.WALL
    maze.unpicked.append(picked_cell)

    maze.pointer.type = Cell.TEMP
    maze.pointer.convert_connections(Cell.TEMP)
    
    for y in range(len(maze.cells)):
        for x in range(len(maze.cells[y])):
            if maze.cells[y][x].type == Cell.TEMP:
                maze.cells[y][x].type = Cell.FLOOR
                maze.cells[y][x].convert_connections(Cell.FLOOR)
                maze.unpicked.remove(maze.cells[y][x])
                maze.picked.append(maze.cells[y][x])

    return 'StartPath'


def set_grid(maze: Maze) -> list:
    grid_size = maze.size * 2 + 1

    grid = []
    for y in range(grid_size):
        grid.append([])
        for x in range(grid_size): 
            if x == 0 or y == 0 or x == grid_size-1 or y == grid_size-1:
                grid[y].append(Cell.WALL)
            elif x % 2 == 0 and y % 2 == 0:
                grid[y].append(Cell.WALL)
            else:
                #grid[y].append(Cell.FLOOR)
                mx = int((x-1)/2)
                my = int((y-1)/2)

                if y % 2 == 1 and x % 2 == 1:
                    grid[y].append(maze.cells[my][mx].type)
                elif x % 2 == 0:
                    grid[y].append(maze.cells[my][mx].connections['E'])
                elif y % 2 == 0:
                    grid[y].append(maze.cells[my][mx].connections['S'])


    #for row in grid:
    #    print(row)
    #    print()

    return grid 




if __name__ == "__main__":
    my_maze = create_maze(5)
    state = "Init"
    counter = 0
    while state != "Finished":
        state = generate_maze(state, my_maze, counter)
    print("Finished generating maze")

    draw_maze(my_maze)
