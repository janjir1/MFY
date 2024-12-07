import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import csv, time



def simulate_GR(m_neutron: int, x0: float, y0: float, vx0: float, vy0: float, Rs: float, target_time: float, resolution: float, save_every: int = 100, c=299792458):

    # Convert Cartesian coordinates to polar coordinates
    def cartesian_to_polar(x, y, vx, vy, mass):
        r = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        pr = mass * (vx * np.cos(phi) + vy * np.sin(phi))
        pphi = mass * r * (-vx * np.sin(phi) + vy * np.cos(phi))
        return r, phi, pr, pphi

    # Equations of motion in Schwarzschild spacetime
    def geodesic_equations(t, y, mass, Rs):
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

    start_time = time.time()
    # Convert to polar coordinates
    r0, phi0, pr0, pphi0 = cartesian_to_polar(x0, y0, vx0, vy0, m_neutron)

    # Initial state vector
    y0 = [r0, phi0, pr0, pphi0]

    # Time span for integration
    t_span = (0, target_time)
    t_eval = np.linspace(t_span[0], t_span[1], int(resolution))

    # Solve the system using solve_ivp
    sol = solve_ivp(
        geodesic_equations,
        t_span,
        y0,
        method='DOP853',
        t_eval=t_eval,
        args=(m_neutron, Rs,),
        rtol=2.220446049250313e-14,
        atol=1e-21

    )

    print(f"GR method solved in: {time.time() - start_time}s")

    # Extract results
    r, phi = sol.y[0], sol.y[1]
    pr, pphi = sol.y[2], sol.y[3]
    times = sol.t

    # Compute Cartesian coordinates
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    # Compute Lorentz factor
    f = 1 - Rs / r  # Schwarzschild metric coefficient
    dr_dt = pr / (m_neutron * f)
    dphi_dt = pphi / (m_neutron * r**2)
    v = np.sqrt(dr_dt**2 + (r * dphi_dt)**2)
    v = np.minimum(v, c - 1e-7)
    lorentz_factors = 1 / np.sqrt(1 - v**2 / c**2)

    # Write results to CSV (every 100th value)
    with open("GR.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(["Time (s)", "x (m)", "y (m)", "Lorentz Factor"])
        # Write the data rows, taking every 100th value
        for t, x_val, y_val, gamma in zip(times[::save_every], x[::save_every], y[::save_every], lorentz_factors[::save_every]):
            writer.writerow([t, x_val, y_val, gamma])

    print(f"GR method finished in: {time.time() - start_time}s")

    if __name__ == "__main__":
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

if __name__ == "__main__":

    # Constants
    G = 6.67430e-11  # Gravitational constant
    M_sun = 1.989e30
    c = 299792458 

    mass1 = 10 * M_sun
    Rs = 2 * G * mass1 / c**2

    m_neutron = 1.675e-27
    position = [2 * Rs, 0]
    velocity = [0, -0.4*c]

    target_time = 0.0003
    
    resolution = 1e6

    simulate_GR(m_neutron, position[0], position[1], velocity[0], velocity[1], Rs, target_time, resolution)
