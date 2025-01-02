import pygame, sys
# Import the classes we've made 
from Classes import Ball

# Colour variables 
BACKGROUND_COLOR = "white"

# Window dimensions. Set up the window, and a clock
WIDTH, HEIGHT = 720, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


# Create a ball object
object = Ball(360, 360, 20)

quit_app = False

# Main simulation loop
while (not quit_app):
    
    # Handle input
    for event in pygame.event.get():
        # Exit when you press the X
        if event.type == pygame.QUIT:
            quit_app = True

    # Fill the window with a solid colour
    WINDOW.fill(BACKGROUND_COLOR)
    
    # Render the ball at its position
    pygame.draw.circle(WINDOW, "blue", (object.pos.x, object.pos.y), object.radius, 1)

    # Update the window
    pygame.display.update()
    CLOCK.tick(300)

# Close the application when the main loop exits
pygame.quit()
sys.exit()