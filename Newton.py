import numpy as np
import csv
from numba import njit, float64
from numba.types import Tuple
import time, sys

def simulate_newton(mass1: int, position1: list, velocity1: list, mass2: int, position2: list, velocity2: list, target_time: float, dt: float, save_every: int = 100, G: float = 6.67430e-11):
    @njit(Tuple((float64[:], float64[:]))(float64, float64[:], float64, float64[:]), cache = True)
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

    @njit(Tuple((float64[:], float64[:]))(float64, float64[:],  float64[:],  float64[:], float64), cache = True)
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
    
    start_time = time.time()

    body1 = Body(
        mass=mass1,
        position=position1,
        velocity=velocity1
    )

    body2 = Body(
        mass=mass2,
        position=position2,
        velocity=velocity2
    )

    with open("Newton.csv", "w", newline="") as file:
        writer = csv.writer(file)
        buffer = []
        buffer_size = 1e4
        sim_time = 0.0
        writer.writerow(["time","x1","y1","x2","y2"])
        counter = 0

        while sim_time<target_time:

            # Calculate gravitational force on each body

            body1.calculate_gravitational_force_wrap(body2)

            # Update positions of both bodies
            
            sim_time += dt
            counter +=1
            body1.update_position_wrap(dt)
            body2.update_position_wrap(dt)

            if counter == save_every:
                data = [sim_time, body1.position[0], body1.position[1], body2.position[0], body2.position[1]]
                buffer.append(data)
                counter = 0

            #print(sim_time)

            if len(buffer) >= buffer_size:
                writer.writerows(buffer)
                buffer.clear()

        if buffer:
            writer.writerows(buffer)                    
            
    print(f"Newton method finished in: {time.time() - start_time}s")


if __name__ == "__main__":
    # Constants
    G = 6.67430e-11  # Gravitational constant
    M_sun = 1.989e30
    c = 299792458 
    
    mass1 = 10 * M_sun
    position1 = [0, 0]
    velocity1 = [0, 0]
    Rs = 2 * G * mass1 / c**2

    mass2 = 1.675e-27
    position2 = [2 * Rs, 0]
    velocity2 = [0, -0.4*c]

    target_time = 0.0003
    dt = 0.0000000003

    simulate_newton(mass1, position1, velocity1, mass2, position2, velocity2, target_time, dt)
