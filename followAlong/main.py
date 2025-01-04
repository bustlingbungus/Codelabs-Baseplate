import pygame, sys
# Import game code
from Cell import *
from Functions import *

createGrid()

quit_app = False

# Main window loop
while not quit_app:
    
    # Handle inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_app = True
        else:
            getInput(event)
    
    # Clear window
    WINDOW.fill("black")
    
    render()
    
    # update the display
    pygame.display.update()
    
# close the application
pygame.quit()
sys.exit()