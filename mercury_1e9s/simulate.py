from Newton import simulate_newton
from Schwarzschild import simulate_GR
from visualize import plot

# Constants
G = 6.67430e-11  # Gravitational constant
M_sun = 1.989e30
c = 299792458 

mass1 = 1 * M_sun
position1 = [0, 0]
velocity1 = [0, 0]
Rs = 2 * G * mass1 / c**2
raduis = 696340000

mass2 = 0.33010e24
position2 = [46e9, 0]
velocity2 = [0, 58.97e3]

target_time = 1e9
resolution = 1e8
dt = target_time/resolution

simulate_GR(mass2, position2[0], position2[1], velocity2[0], velocity2[1], Rs, target_time, resolution)

simulate_newton(mass1, position1, velocity1, mass2, position2, velocity2, target_time, dt)

body1_file = "Newton.csv"
body2_file = "GR.csv"

# Set up simulation parameters
limit = 80000000000  # Adjust plot limits
interval = 50e-8  # Update interval in milliseconds
tick = 5e6

plot(body1_file, body2_file, limit, interval, raduis, "Event horizon", export_animation=False)