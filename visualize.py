import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib import ticker
from matplotlib.ticker import EngFormatter


def plot(body1_file, body2_file, limit, tick, body_radius, body_name):
        # Read data from files
    def read_csvN(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Skip header if present
            next(reader, None)
            data = []
            for row in reader:
                timestamp, _, _, x, y = map(float, row)
                data.append((timestamp, x, y))
            return data
        
    def read_csvG(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Skip header if present
            next(reader, None)
            data = []
            for row in reader:
                timestamp, x, y, _ = map(float, row)
                data.append((timestamp, x, y))
            return data

    # Load data for both bodies
    body1_data = read_csvN(body1_file)
    body2_data = read_csvG(body2_file)

    # Extract paths for plotting
    body1_path_x = [point[1] for point in body1_data]  # X-coordinates
    body1_path_y = [point[2] for point in body1_data]  # Y-coordinates
    body2_path_x = [point[1] for point in body2_data]  # X-coordinates
    body2_path_y = [point[2] for point in body2_data]  # Y-coordinates

    # Initialize plot
    fig, ax = plt.subplots()
    ax.plot(body1_path_x, body1_path_y, 'b--', label='Newton Path')  # Dotted blue line for Body 1 path
    ax.plot(body2_path_x, body2_path_y, 'r--', label='GR Path')  # Dotted red line for Body 2 path
    body1, = ax.plot([], [], 'bo', label='Newton')  # Blue circle for Body 1
    body2, = ax.plot([], [], 'ro', label='GR')  # Red circle for Body 2
    ax.legend()

    # Set plot limits
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    circle = plt.Circle((0, 0), body_radius, color='black', fill=True, label=body_name)
    ax.add_artist(circle)


    # Enable grid and set up major and minor ticks
    ax.grid(True)
    formatter1 = EngFormatter(places=0, sep="", unit="m")
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/limit*tick:.0f}'))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter1))
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y/limit*tick:.0f}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter1))

    # Display text for simulation time
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    # Initialize frame index
    frame_index = 0
    last_x1, last_y1 = None, None
    last_x2, last_y2 = None, None

    def init():
        body1.set_data([], [])
        body2.set_data([], [])
        time_text.set_text('')
        return body1, body2, time_text

    def update(frame):
        nonlocal frame_index, last_x1, last_y1, last_x2, last_y2

        # If data exists for Body 1, update it; otherwise, keep it at the last known position
        if frame_index < len(body1_data):
            t1, x1, y1 = body1_data[frame_index]
            body1.set_data([x1], [y1])
            last_x1, last_y1 = x1, y1  # Update last known position
        else:
            body1.set_data([last_x1], [last_y1])  # Use last known position

        # If data exists for Body 2, update it; otherwise, keep it at the last known position
        if frame_index < len(body2_data):
            t2, x2, y2 = body2_data[frame_index]
            body2.set_data([x2], [y2])
            last_x2, last_y2 = x2, y2  # Update last known position
        else:
            body2.set_data([last_x2], [last_y2])  # Use last known position

        # Synchronize time display to the maximum available timestamp
        current_time = max(
            body1_data[frame_index][0] if frame_index < len(body1_data) else 0,
            body2_data[frame_index][0] if frame_index < len(body2_data) else 0
        )
        formatter2 = EngFormatter(places=0, sep="", unit="s")
        formatted_time = formatter2.format_eng(current_time)
        time_text.set_text(f'Simulation Time: {formatted_time}s')

        frame_index += 1
        return body1, body2, time_text

    # Animation
    ani = animation.FuncAnimation(fig, update, init_func=init,
                                blit=True, interval=interval, cache_frame_data=False)


    # Enable interactive pan/zoom in the plot
    plt.gca().set_aspect('auto', adjustable='box')
    fig.canvas.toolbar_visible = True  # Shows the interactive toolbar with pan and zoom options
    ax.set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    # File paths for body data
    body1_file = "Newton.csv"
    body2_file = "GR.csv"

    # Set up simulation parameters
    limit = 75000  # Adjust plot limits
    interval = 5e-3  # Update interval in milliseconds

    G = 6.67430e-11  # Gravitational constant
    M_sun = 1.989e30
    c = 299792458 
    mass1 = 10 * M_sun
    Rs = 2 * G * mass1 / c**2
    tick = 1e6

    plot(body1_file, body2_file, limit, tick, Rs, "event")