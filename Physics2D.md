author: Caden Spokas
summary:
id: Physics2dCodelab
tags:
categories:
environments: Web
status: Published
feedback link: https://github.com/bustlingbungus/Codelabs-Baseplate/tree/Physics_2D

# 2D Physics Simulation

## Overview

### Table of Contents

1. 

### Final Simulation

![Final Simulation](img/finalProduct.gif)

## Setting Up Environment

### VSCode and Python

We will be using VSCode to create the Python code for this project. These can be downloaded here:
* [VSCode](https://code.visualstudio.com/download)
* [Python](https://www.python.org/downloads/) 

> aside positive
> If you use some IDE other than VSCode, that should be fine!

### Make sure to check this box here:

![Python Instruction](img/pythonAddToPath.png)

### Pygame 

This project will use an API called `pygame` to create a window and render things onto it. To get pygame, just type the following command in a VSCode terminal:

For Windows:

``` bash
py -m pip install -U pygame --user
```

For Mac:

``` bash
python3 -m pip install -U pygame --user
```

Create a new folder on your computer for this project, and open it in VSCode.

## Creating an Individual Game Object

### Create two files

This project will be split between two files. One for the management code, and one for class definitions. In your folder, create
* main.py
* Classes.py

### main.py (pygame boilerplate)

This is just a baseplate for opening a window in pygame. We'll be modifying this as we develop the project

``` Python
import pygame, sys

# Colour variables 
BACKGROUND_COLOR = "white"

# Window dimensions. Set up the window, and a clock
WIDTH, HEIGHT = 720, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

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

    # Update the window
    pygame.display.update()
    CLOCK.tick(300)

# Close the application when the main loop exits
pygame.quit()
sys.exit()
```

### Classes.py (entity definition)

In this simulation, we're going to make circles that bounce around the window. Each of these balls will have a position, and a radius, so in `Classes.py`, let's define a class for them like this:

``` Python
# A class for a collision object
class Ball:
    # Initialise position and radius
    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.radius = radius
```

### Adding a ball in main.py

To add an individual ball onto the window, go back to `main.py`, and include this class definition. Then create a ball object and render it every frame.

``` Python
# Create a ball object
object = Ball(360, 360, 20)         # <------------- ADD THIS LINE HERE

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
    pygame.draw.circle(WINDOW, "blue", (object.x, object.y), object.radius, 1)      # <------------- ADD THIS LINE HERE

    # Update the window
    pygame.display.update()
    CLOCK.tick(300)
```

### When you run `main.py`, there should now be a circle in the middle of the window.

![Single Circle on the Window](img/singleBallSlide3.PNG)

## Creating the Vector2 class

To represent position in 2D space, the x and y coordinates can be made into a 2D vector. Creating a class for a 2D vector will be useful because we can organise an x,y pair into one object, and we can add class functions like `length` to find vector magnitude, and overload operators to make vector arithmetic easier.

Go to `Classes.py`, and before the `Ball` class definition, create a `Vector2` class:

``` Python
# Define a structure to represent 2D position, velocity, and acceleration
class Vector2:
    
    # Initialise x and y variables 
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
```

For later use in this project, we're going to need to find the magnitude of a vector, as well as create unit vectors (which is a vector whose magnitude is 1).

We're also going to overload operators to allow for arithmetic between two vector objects, using traditional operators, like `+` and `*`.

Add these functions to the `Vector2`: 

``` Python
from math import sqrt       # <-------- ADD THIS LINE HERE

# Define a structure to represent 2D position, velocity, and acceleration
class Vector2:
    
    # Initialise x and y variables 
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y

    # |                        |
    # |   ADD THESE FUNCTIONS  |
    # V                        V

    # The magnitude of the vector is sqrt(x^2 + y^2)
    def length(self):
        return sqrt((self.x**2) + (self.y**2))
    
    # Make the vector's length 1 by dividing x and y by the length
    def normalize(self):
        leng = self.length()
        self.x /= leng
        self.y /= leng

    # Redefine basic operators to make vector arithmetic easier
    
    # Redefine - to return this vector minus the other vector
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    # Redefine -= to subtract the other vector's x and y components from this one
    def __isub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    # Redefine += to add the other vector's x and y components to this one
    def __iadd__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
        
    # Redefine * to return x and y multiplied by k
    def __mul__(self, k):
        return Vector2(self.x * k, self.y * k)
```
> aside negative
> We could add other operator overloads for things like scalar division, the dot product, etc. I wanted to reduce clutter though, since those operations aren't used in this project. See if you can implement them! :)

### Give the Ball class Vector2 members

Let's replace the `Ball` class' position with one Vector2, and add a velocity and acceleration vector to the class as well.

* In `Classes.py`:

``` Python
# A class for a collision object
class Ball:
    # Initialise position, velocity, acceleration, and radius
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)            # <------ ADD THIS LINE HERE
        self.velocity = Vector2(0, 0)       # <------ ADD THIS LINE HERE
        self.acceleration = Vector2(0, 0)   # <------ ADD THIS LINE HERE
        
        self.radius = radius
```

* In `main.py`:

``` Python
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
    # |                  |
    # | MODIFY THIS LINE |
    # V                  V
    pygame.draw.circle(WINDOW, "blue", (object.pos.x, object.pos.y), object.radius, 1)

    # Update the window
    pygame.display.update()
    CLOCK.tick(300)
```