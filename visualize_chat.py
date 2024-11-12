import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import matplotlib.ticker as ticker

def data_generator(filename, skip_lines=30):
    """Yields each line of data from a CSV file, skipping lines based on the skip_lines parameter."""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Skip lines according to the skip_lines parameter
            if i % skip_lines == 0:
                # Scale positions by 10^9
                yield (float(row['time']), float(row['x1']), float(row['y1']),
                       float(row['x2']), float(row['y2']))

def animate_bodies(filename, initial_fps=30, skip_lines=30):
    interval = 1000 / initial_fps  # Time in milliseconds between frames

    # Initialize plot
    fig, ax = plt.subplots()
    body1, = ax.plot([], [], 'bo', label='Body 1')  # Blue circle for Body 1
    body2, = ax.plot([], [], 'ro', label='Body 2')  # Red circle for Body 2
    ax.legend()

    # Set plot limits (adjusted for the 10^9 scaling factor)
    ax.set_xlim(-1e9, 1e9)
    ax.set_ylim(-1e9, 1e9)
    
    # Enable grid and set up major and minor ticks
    ax.grid(True)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e9:.0f}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y/1e9:.0f}'))

    # Initialize data generator with skip_lines based on initial_fps
    data_gen = data_generator(filename, skip_lines)
    current_data = next(data_gen, None)

    # Display text for simulation time
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        body1.set_data([], [])
        body2.set_data([], [])
        time_text.set_text('')
        return body1, body2, time_text

    def update(frame):
        nonlocal current_data, data_gen

        # Get next data point
        current_data = next(data_gen, None)
        # Reset generator if we reach the end of data
        if current_data is None:
            data_gen = data_generator(filename, int(fps_slider.val - 1))  # Reset generator with updated skip_lines
            current_data = next(data_gen, None)

        # Update body positions and time if data is available
        if current_data:
            sim_time, x1, y1, x2, y2 = current_data
            body1.set_data([x1], [y1])  # Wrap x1, y1 in lists
            body2.set_data([x2], [y2])  # Wrap x2, y2 in lists
            time_text.set_text(f'Simulation Time: {sim_time:.2f} s')  # Display simulation time
        return body1, body2, time_text

    ani = animation.FuncAnimation(fig, update, init_func=init,
                                  blit=True, interval=interval, cache_frame_data=False)

    # Create an axis for the slider
    slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03], facecolor="lightgoldenrodyellow")
    fps_slider = Slider(slider_ax, "FPS", 1, 60, valinit=initial_fps, valstep=1)

    # Update the animation interval and skip_lines when the slider value changes
    def update_fps(val):
        ani.event_source.interval = 1000 / fps_slider.val
        nonlocal data_gen, current_data
        data_gen = data_generator(filename, int((fps_slider.val - 1)*10))  # Reset generator with new skip_lines
        current_data = next(data_gen, None)  # Load first data point with new skip_lines

    fps_slider.on_changed(update_fps)

    # Enable interactive pan/zoom in the plot
    plt.gca().set_aspect('auto', adjustable='box')
    fig.canvas.toolbar_visible = True  # Shows the interactive toolbar with pan and zoom options

    plt.show()


if __name__ == "__main__":
    animate_bodies("Newton.csv", 30)
