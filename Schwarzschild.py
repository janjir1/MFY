import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
c = 3.0e8         # Speed of light, m/s
M_sun = 1.989e30  # Solar mass, kg

# Black hole parameters
M = 10 * M_sun  # Mass of the black hole (10 solar masses)
Rs = 2 * G * M / c**2  # Schwarzschild radius

# Equations of motion in Schwarzschild spacetime
def geodesic_equations(t, y):
    r, phi, pr, pphi = y  # Position (r, phi) and momenta (pr, pphi)

    # Effective potential terms
    f = 1 - Rs / r  # Schwarzschild metric coefficient

    # Derivatives of coordinates
    dr_dt = pr / f  # Radial momentum to radial velocity
    dphi_dt = pphi / r**2  # Angular momentum to angular velocity
    
    # Derivatives of momenta
    dpr_dt = -M * c**2 * Rs / (2 * r**2 * f) + pphi**2 / r**3  # Radial force
    dpphi_dt = 0  # Angular momentum conservation
    
    return [dr_dt, dphi_dt, dpr_dt, dpphi_dt]

# Initial conditions
r0 = 20 * Rs  # Start further away from the black hole
phi0 = 0.0  # Initial angle
pr0 = -0.6 * c  # Initial radial velocity (towards the black hole)
pphi0 = 5.0 * Rs * c  # Initial angular momentum (non-zero to avoid direct plunge)

# Initial state vector
y0 = [r0, phi0, pr0, pphi0]

# Time span for integration
t_span = (0, 1e4)  # Increased time span
t_eval = np.linspace(t_span[0], t_span[1], 10000)

# Solve the system using solve_ivp
sol = solve_ivp(geodesic_equations, t_span, y0, method='RK45', t_eval=t_eval)

# Extract results
r, phi = sol.y[0], sol.y[1]

# Convert to Cartesian coordinates for visualization
x = r * np.cos(phi)
y = r * np.sin(phi)

# Plot the trajectory
plt.figure(figsize=(8, 8))
plt.plot(x, y, label='Neutron Trajectory')
plt.scatter(0, 0, color='black', label='Black Hole (Rs)')
circle = plt.Circle((0, 0), Rs, color='black', fill=True, label='Event Horizon')
plt.gca().add_artist(circle)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Neutron Trajectory Near a Black Hole")
plt.legend()
plt.axis("equal")
plt.xlim([-3e10, 3e10])  # Adjust x-limits to ensure the path is visible
plt.ylim([-3e10, 3e10])  # Adjust y-limits to ensure the path is visible
plt.grid()
plt.show()
