import numpy as np
import csv
from numba import njit, float64
from numba.types import Tuple
import time

# Constants
G = 6.67430e-11  # Gravitational constant
SPEED = 10

@njit(Tuple((float64[:], float64[:]))(float64, float64[:], float64, float64[:]), cache = True, fastmath = True)
def calculate_gravitational_force(mass1, position1, mass2, position2):
    # Calculate distance vector and squared distance
    DPosition = position2 - position1
    distance_squared = np.dot(DPosition, DPosition)

    # Collision check
    if distance_squared == 0:
        raise ValueError("Distance between bodies cannot be zero.")

    # Calculate force magnitude and vector
    force_magnitude = G * mass1 * mass2 / distance_squared
    force_vector = force_magnitude * (DPosition / np.sqrt(distance_squared))
    
    return force_vector, -force_vector

@njit(Tuple((float64[:], float64[:]))(float64, float64[:],  float64[:],  float64[:], float64), cache = True, fastmath = True)
def update_position(mass, position, velocity, force_vector, dt):
    # Calculate acceleration
    acceleration = force_vector / mass

    # Update velocity and position
    velocity += acceleration * dt
    position += velocity * dt

    return position, velocity

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.force_vector = np.zeros(3, dtype=np.float64)

    def calculate_gravitational_force_wrap(self, other):
        self.force_vector, other_force_vector = calculate_gravitational_force(
            self.mass, self.position, other.mass, other.position
        )
        other.set_gravitational_force(other_force_vector)

    def set_gravitational_force(self, force):
        self.force_vector = force

    def update_position_wrap(self, dt):
        self.position, self.velocity = update_position(
            self.mass, self.position, self.velocity, self.force_vector, dt
        )

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


start_time = time.time()

with open("Newton.csv", "w", newline="") as file:
    writer = csv.writer(file)
    buffer = []
    buffer_size = 1e4
    sim_time = 0.0
    target_time = 1e5
    #writer.writerow(["time","x1","y1","x2","y2"])
    dt = 1 / SPEED

    while sim_time<target_time:

        # Calculate gravitational force on each body

        body1.calculate_gravitational_force_wrap(body2)

        # Update positions of both bodies
        
        sim_time += dt
        body1.update_position_wrap(dt)
        body2.update_position_wrap(dt)

        data = [sim_time, body1.position[0], body1.position[1], body2.position[0], body2.position[1]]
        buffer.append(data)

        #print(sim_time)

        if len(buffer) >= buffer_size:
            #print(sim_time)
            writer.writerows(buffer)
            buffer.clear()

    if buffer:
        writer.writerows(buffer)                    
        


print(f"this took {time.time() - start_time}s")
 