from Newton import simulate_newton
from Schwarzschild import simulate_GR
from visualize import plot

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
resolution = 1e7
dt = target_time/resolution

simulate_GR(mass2, position2[0], position2[1], velocity2[0], velocity2[1], Rs, target_time, resolution)

simulate_newton(mass1, position1, velocity1, mass2, position2, velocity2, target_time, dt)

body1_file = "Newton.csv"
body2_file = "GR.csv"

# Set up simulation parameters
limit = 75000  # Adjust plot limits
interval = 0.05e-3  # Update interval in milliseconds
tick = 1e6

plot(body1_file, body2_file, limit, interval, Rs, "Event horizon", False)