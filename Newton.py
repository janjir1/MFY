import numpy as np
import csv

# Constants
G = 6.67430e-11  # Gravitational constant
SPEED = 1

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.force_vector = np.empty(1, dtype=float)

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

        other.set_gravitational_force(self.force_vector * -1)

    def set_gravitational_force(self, force):
        self.force_vector = force

    def update_position(self, dt):

        # Calculate acceleration
        acceleration = self.force_vector / self.mass

        # Update velocity and position
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

    def export_data(self):
        return self.position, self.velocity
    

 
 # Define two bodies with initial properties

body1 = Body(
    mass=5.972e24,
    position=[-1.5e8, 1e6],  # Positioned to the left of the screen center
    velocity=[0, 0],    # Increased velocity for visibility
)
body2 = Body(
    mass=7.348e22,
    position=[1.5e8, -1e6],  # Positioned to the right of the screen center
    velocity=[0, 100],    # Increased velocity for visibility
)



running = True

with open("Newton.csv", "a", newline="") as file:
    writer = csv.writer(file)
    buffer = []
    buffer_size = 1000
    i=0
    time = 0
    target_time = 1e6
    writer.writerow(["time","x1","y1","x2","y2"])

    while time<target_time:

        # Calculate gravitational force on each body

        body1.calculate_gravitational_force(body2)

        # Update positions of both bodies
        dt = 1 / SPEED
        time += dt
        body1.update_position(dt)
        body2.update_position(dt)

        data = [time, body1.position[0], body1.position[1], body2.position[0], body2.position[1]]
        buffer.append(data)

        print(time)

        if len(buffer) >= buffer_size:
            writer.writerows(buffer)
            buffer.clear()

    if buffer:
        writer.writerows(buffer)
 