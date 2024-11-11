import numpy as np

# Constants
G = 6.67430e-11  # Gravitational constant
SPEED = 1e6

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def calculate_gravitational_force(self, other):

        # Calculate distance
        DPosition = other.position - self.position
        distance_squared = np.dot(DPosition, DPosition)

        # Colision
        if distance_squared == 0:
            raise ValueError("Distance between bodies cannot be zero.")

        # Calculate force
        force_magnitude = G * self.mass * other.mass / distance_squared
        self.force_vector = force_magnitude * (DPosition / np.sqrt(distance_squared))

        other.set_gravitational_force([-self.force_vector[0], -self.force_vector[1]])

    def set_gravitational_force(self, force):
        self.force_vector = force

    def update_position(self, dt):

        print(self.force_vector)
        # Calculate acceleration
        acceleration = self.force_vector / self.mass

        # Update velocity and position
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
    

 
 # Define two bodies with initial properties

body1 = Body(
    mass=5.972e24,
    position=[-1.5e8, 0],  # Positioned to the left of the screen center
    velocity=[0, 0],    # Increased velocity for visibility
)
body2 = Body(
    mass=7.348e22,
    position=[1.5e8, 0],  # Positioned to the right of the screen center
    velocity=[0, 1000],    # Increased velocity for visibility
)



running = True
while running:

    # Calculate gravitational force on each body

    body1.calculate_gravitational_force(body2)

    # Update positions of both bodies
    dt = 1 / SPEED
    body1.update_position(dt)
    body2.update_position(dt)

