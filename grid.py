import pygame

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
PALEVIOLETRED = (219,112,147)
LAVENDER = (230,230,250)
LIME = (0,255,0)
CADETBULUE = (95,158,160)
ORANGE = (255,165,0)

pygame.display.set_caption("Grid")


# a spot is a square whose width and height are the same
class Spot: 
    def __init__(self, row, col, width, color):
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.color = self.original_color = color 
        self.neighbors = []
    
    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.color == LIME
    
    def make_start(self):
        self.color = LIME

    def is_end(self):
        return self.color == GOLD

    def make_end(self):
        self.color = GOLD

    def is_barrier(self):
        return self.color == CADETBULUE

    def make_barrier(self):
        self.color = CADETBULUE

    def is_closed(self):
        return self.color == BEIGE

    def make_closed(self):
        self.color = BEIGE

    def is_open(self):
        return self.color == PINK

    def make_open(self):
        self.color = PINK

    def make_path(self):
        self.color = ORANGE

    def reset(self):
        self.color = self.original_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, grid_rows, grid_cols):
        self.neighbors = []
        
        if not self.row == grid_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN (except for the bottom border)
            self.neighbors.append(grid[self.row + 1][self.col])

        if not self.row == 0 and not grid[self.row - 1][self.col].is_barrier(): # UP (except for the top border)
            self.neighbors.append(grid[self.row - 1][self.col])

        if not self.col == grid_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT (except for the right border)
            self.neighbors.append(grid[self.row][self.col + 1] )

        if not self.col == 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT (except for the left border)
            self.neighbors.append(grid[self.row][self.col - 1])
    
    # TODO - why do we need this func here?
    # def __lt__(self, other): #Less Than
    #     return False

class GridLine:
    def __init__(self, total_rows, total_cols, win_width, win_height, color):
        self.rows = total_rows
        self.cols = total_cols
        self.win_width = win_width
        self.win_height = win_height
        self.width = win_width / total_cols
        self.height = win_height / total_rows
        self.color = color

    def draw(self, win):
        for i in range(self.rows): # draw horizontal lines
            pygame.draw.line(win, self.color, (0, i*self.height), (self.win_width, i*self.height))
        for j in range(self.cols): # draw vertical lines
            pygame.draw.line(win, self.color, (j*self.width, 0), (j*self.width, self.win_height))


# make a grid of given total rows, cols and also the size of each spot
def make_spot_grid(total_rows, total_cols, spot_width, spot_color=WHITE):
    grid = [] # a 2D array simulating the grid of spots
    for i in range(total_rows):
        grid.append([])
        for j in range(total_cols):
            spot = Spot(i, j, spot_width, spot_color)
            grid[i].append(spot)

    return grid
     

# draw all the spots (marked/unmarked) and the grid lines
def draw_spot_grid(win, win_width, win_height, rows, cols, grid, line_color=PLUM):
    win.fill(WHITE)
    
    # draw every single marked spots
    for row in grid:
        for spot in row:
            spot.draw(win)

    # draw the grid line on top of the grids of spots to make it appear
    grid_line = GridLine(rows, cols, win_width, win_height, line_color)
    grid_line.draw(win)

    pygame.display.update()



def main(): 
    # pygame display
    WIN_WIDTH = 600
    WIN_HEIGHT = 600
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    SPOT_WIDTH = 20
    TOTOAL_ROWS = WIN_HEIGHT // SPOT_WIDTH
    TOTAL_COLS = WIN_WIDTH // SPOT_WIDTH
    
    grid = make_spot_grid(TOTOAL_ROWS, TOTAL_COLS, SPOT_WIDTH)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        draw_spot_grid(WIN, WIN_WIDTH, WIN_HEIGHT, TOTOAL_ROWS, TOTAL_COLS, grid)
    pygame.quit()


# TODO - test general grid functionality with unit test
# make general grid with customized width and height of the elements
def draw_grid():
     # pygame display
    WIN_WIDTH = 700
    WIN_HEIGHT = 500
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    WIN.fill(TURQUOISE)
    
    TOTOAL_ROWS = 3
    TOTAL_COLS = 10
    
    grid = GridLine(TOTOAL_ROWS, TOTAL_COLS, WIN_WIDTH, WIN_HEIGHT, PLUM)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        grid.draw(WIN)
        pygame.display.update()

    pygame.quit()
    

if __name__ == '__main__':
    # draw_grid()
    main()