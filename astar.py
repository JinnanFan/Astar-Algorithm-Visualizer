import pygame
from queue import PriorityQueue
from grid import draw_spot_grid as draw_grid
from grid import make_spot_grid as make_grid


# Settings for the display window
WIDTH = 1000
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

# Color options
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128,0)
GOLD = (255, 215, 0)
ROSYBROWN = (188, 143, 143)
TURQUOISE = (64, 224, 208)
PLUM = (221, 160, 221)
BEIGE = (245, 245, 220) 
PINK = (255, 192, 203)
LAVENDER = (230,230,250)

        
# use mouse to mark each spot as Start Node, End Node, or barriers
def mark_spot(grid, spot_width, start, end):
    if pygame.mouse.get_pressed()[0]: # LEFT mouse button
        row, col = get_clicked_pos(spot_width)
        spot = grid[row][col]
        if not start:
            start = spot
            start.make_start()
        elif not end and spot != start:
            end = spot
            end.make_end()
        elif spot != start and spot != end:
            spot.make_barrier()

    elif pygame.mouse.get_pressed()[2]: # RIGHT mouse button
        row, col = get_clicked_pos(spot_width)
        spot = grid[row][col]
        if spot.is_start():
            start = None
        elif spot.is_end():
            end = None
        spot.reset()

    return grid, start, end



# help to convert the mouse clicked position into row and col position of the grids
def get_clicked_pos(gap):
    pos = pygame.mouse.get_pos()
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col
    

def astar(draw, grid, start, end):
    pause = False
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = set()
    open_set_hash.add(start) # open_set_hash = {start}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = 0
    came_from = {}

    EDGE_WEIGHT = 1

    current = start
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]: # PAUSE
                    pause = True
                if pygame.key.get_pressed()[pygame.K_s]: # START
                    pause = False   
                if pygame.key.get_pressed()[pygame.K_q]: # QUITE
                    return False # quite current algorithm loops and return to main func (but will not reset the grid/start/end)
                if pygame.key.get_pressed()[pygame.K_r]: # RESET
                    return False # quite current algorithm loops and return to main func (also, in main func, followed with the reset steps of grid/start/end)

        if not pause:
            if current == end:
                reconstruct_path(draw, came_from, end) # find the shortest path and display it
                end.make_end()
                start.make_start()
                return True

            current = open_set.get()[2]
            open_set_hash.remove(current)
            if current != start:
                current.make_closed()
            for neighbor in current.neighbors:
                new_g_score = g_score[current] + EDGE_WEIGHT
                if new_g_score < g_score[neighbor]:
                    g_score[neighbor] = new_g_score # update g score
                    h_score = h(neighbor.get_pos(), end.get_pos())
                    f_score[neighbor] = g_score[neighbor] + h_score
                    
                    if not neighbor in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
                        came_from[neighbor] = current
                    '''
                    For each node considered (the "neighbor" here), its h score is always the same. Hence, its f score will be updated only if its g score updated, which means only when the g score of the node gets smaller, the node will be added into the open set for later use.
                    '''
                draw()
    return False


def h(p1, p2): # heuristic fuction implemented with Manhattan distance beteen the current spot to the end spot
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)
    

def reconstruct_path(draw, came_from, current):
    while current in came_from: # start node is not in came_from (it is not one of the keys of came_from dictionary) 
        current.make_path()
        current = came_from[current]
        draw()
   

def main(win, win_width, win_height):
    SPOT_WIDTH = 20
    ROWS = win_height // SPOT_WIDTH
    COLS = win_width // SPOT_WIDTH
    grid = make_grid(ROWS, COLS, SPOT_WIDTH)

    start = None
    end = None

    run = True
    while run:
        draw_grid(win, win_width, win_height, ROWS, COLS, grid) # need to put this draw func before the "for event". Why?
        grid, start, end = mark_spot(grid, SPOT_WIDTH, start, end)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_s] and start and end: # START
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid, ROWS, COLS)        

                    astar(lambda: draw_grid(win, win_width, win_height, ROWS, COLS, grid), grid, start, end)

                if pygame.key.get_pressed()[pygame.K_r]: # RESET
                    start = None
                    end = None
                    grid = make_grid(ROWS, COLS, win_height//ROWS)

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH, HEIGHT)
