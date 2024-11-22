import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import csv

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
c = 3.0e8         # Speed of light, m/s
M_sun = 1.989e30  # Solar mass, kg
m_neutron = 1.675e-27  # Neutron mass, kg

# Black hole parameters
M = 10 * M_sun  # Mass of the black hole (10 solar masses)
Rs = 2 * G * M / c**2  # Schwarzschild radius

# Convert Cartesian coordinates to polar coordinates
def cartesian_to_polar(x, y, vx, vy, mass):
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    pr = mass * (vx * np.cos(phi) + vy * np.sin(phi))
    pphi = mass * r * (-vx * np.sin(phi) + vy * np.cos(phi))
    return r, phi, pr, pphi

# Equations of motion in Schwarzschild spacetime
def geodesic_equations(t, y, mass):
    r, phi, pr, pphi = y  # Position (r, phi) and momenta (pr, pphi)

    # Schwarzschild metric coefficient
    f = 1 - Rs / r

    # Derivatives of coordinates
    dr_dt = pr / (mass * f)
    dphi_dt = pphi / (mass * r**2)

    # Derivatives of momenta
    dpr_dt = -mass * c**2 * Rs / (2 * r**2 * f) + pphi**2 / (mass * r**3)
    dpphi_dt = 0  # Angular momentum conservation

    return [dr_dt, dphi_dt, dpr_dt, dpphi_dt]

# Initial conditions in Cartesian coordinates
x0 = 2 * Rs  # Initial x-position
y0 = 0        # Initial y-position
vx0 = 0       # Initial x-velocity
vy0 = -0.4 * c  # Initial y-velocity
# vy0 = 0 * c  # Initial y-velocity


# Convert to polar coordinates
r0, phi0, pr0, pphi0 = cartesian_to_polar(x0, y0, vx0, vy0, m_neutron)

# Initial state vector
y0 = [r0, phi0, pr0, pphi0]

# Time span for integration
t_span = (0, 1e-2)
t_eval = np.linspace(t_span[0], t_span[1], int(1e12))

# Solve the system using solve_ivp
sol = solve_ivp(
    geodesic_equations,
    t_span,
    y0,
    method='RK45',
    t_eval=t_eval,
    args=(m_neutron,)

)

# Extract results
r, phi = sol.y[0], sol.y[1]
pr, pphi = sol.y[2], sol.y[3]
times = sol.t

print("Simulation complete")

# Compute Cartesian coordinates
x = r * np.cos(phi)
y = r * np.sin(phi)

# Compute Lorentz factor
f = 1 - Rs / r  # Schwarzschild metric coefficient
dr_dt = pr / (m_neutron * f)
dphi_dt = pphi / (m_neutron * r**2)
v = np.sqrt(dr_dt**2 + (r * dphi_dt)**2)
v = np.clip(v, 0, 0.9999 * c)  # Ensure velocity < c
lorentz_factors = 1 / np.sqrt(1 - v**2 / c**2)

print("Data ready")

# Write results to CSV (every 100th value)
with open("neutron_trajectory.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Time (s)", "x (m)", "y (m)", "Lorentz Factor"])
    # Write the data rows, taking every 100th value
    for t, x_val, y_val, gamma in zip(times[::100], x[::100], y[::100], lorentz_factors[::100]):
        writer.writerow([t, x_val, y_val, gamma])

print("Exported")

# Plot the trajectory
plt.figure(figsize=(8, 8))
plt.plot(x, y, label='Neutron Trajectory')
plt.scatter(0, 0, color='black', label='Black Hole (Rs)')
circle = plt.Circle((0, 0), Rs, color='black', fill=True, label='Event Horizon')
plt.gca().add_artist(circle)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Neutron Trajectory Near a Black Hole")
plt.legend(loc='upper right')
plt.axis("equal")
plt.xlim([-1e7, 1e7])  # Adjust x-limits to ensure the path is visible
plt.ylim([-1e7, 1e7])  # Adjust y-limits to ensure the path is visible
plt.grid()
plt.show()
