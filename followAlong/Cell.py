import pygame

# Returns a colour based on the number of bombs surrounding a cell
def getColor(numSurroundingBombs):
    match (numSurroundingBombs):
        case 1: 
            return (50,50,255)
        case 2:
            return (50,255,50)
        case 3: 
            return (255,50,50)
        case 4:
            return (170,0,255)
        case 5: 
            return (255,255,0)
        case 6:
            return (255,150,0)
        case 7: 
            return (20,20,20)
        case 8:
            return (30,0,0)
    return (0,0,0)

# A single cell on the minsweeper board
class Cell:

    # Initialise cell x and y indices, and whether the cell is a bomb
    # Initialise whether the cell is revealed, and whether ir contains a flag
    def __init__(self, isBomb, x, y):
        # If the cell is a bomb, make surrounding bombs -1
        if isBomb:
            self.surrounding_bombs = -1
        else:
            self.surrounding_bombs = 0
            
        self.revealed = False
        self.flagged = False
        
        # x and y represent the indices of the cell
        self.x, self.y = x, y
        
    def isBomb(self):
        return self.surrounding_bombs == -1
        
    # Gets a list of the cells surrounding this one
    def surrounding(self):
        # import array from functions
        from Functions import cells, NX, NY
        surrounding = []
        
        # iterate through the 8 cells surrounding (x, y)
        # skip if the cell is out of bounds, or if the cell *is* (x, y)
        for i in range(self.x-1, self.x+2):
            if not 0<=i<NX: # cell out of bounds
                continue
            for j in range(self.y-1, self.y+2):
                if (not 0<=j<NY) or (j==self.y and i==self.x):
                    continue
                # Add the cell to the surorounding arry
                surrounding.append(cells[i][j])
        # return the array of surrounding cells
        return surrounding
    
    # counts the number of surrounding cells that are bombs
    def countSurrounding(self):
        # do nothing if the cell is a bomb
        if not self.isBomb():
            # reset bomb counter to 0
            self.surrounding_bombs = 0
            # for each bomb in surrounding cells, increment the bomb counter
            for cell in self.surrounding():
                if cell.isBomb():
                    self.surrounding_bombs += 1
                    
    # Makes the cell revealed. If the cells has 0 surrounding bombs, 
    # reveals all adjacent cells
    def reveal(self):
        # make the cell revealed
        self.revealed = True
        # If there are not surrounding bombs, reveal all surrounding
        if self.surrounding_bombs == 0:
            for cell in self.surrounding():
                if not cell.revealed:
                    cell.reveal()
                    
    # Renders the cell onto the screen
    def render(self):
        # get required variables from functions
        from Functions import WINDOW, FONT, CELL_SIZE, FLAG, BOMB
        # Set up a rect to represent the cell's space on the window
        rect = pygame.Rect(self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        # If the cells is revealed, show the number of surrounding bombs, or,
        # if the cell IS a bomb, render the bomb image
        if self.revealed:
            # render cell background
            pygame.draw.rect(WINDOW, (170,170,170), rect)
            
            # render bomb image if the cell is a bomb
            if self.isBomb():
                WINDOW.blit(BOMB, rect)
            # Render a number for the surrounding bomb count
            elif self.surrounding_bombs > 0:
                num = FONT.render(str(self.surrounding_bombs), True, getColor(self.surrounding_bombs))
                num_rect = num.get_rect(center=(rect.x+rect.w/2,rect.y+rect.h/2))
                WINDOW.blit(num, num_rect)

        # If the cell ISN'T revealed, just render the cell backgorund
        # if the cell has a flag, render the flag image
        else:
            pygame.draw.rect(WINDOW, (90,90,90), rect)
            if self.flagged:
                WINDOW.blit(FLAG, rect)