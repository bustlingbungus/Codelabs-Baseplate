from math import sqrt

# Define a structure to represent 2D position, velocity, and acceleration
class Vector2:
    
    # Initialise x and y variables 
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y

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

# A class for a collision object
class Ball:
    # Initialise position, velocity, acceleration, and radius
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)            # <------ ADD THIS LINE HERE
        self.velocity = Vector2(0, 0)       # <------ ADD THIS LINE HERE
        self.acceleration = Vector2(0, 0)   # <------ ADD THIS LINE HERE
        
        self.radius = radius