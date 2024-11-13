import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import matplotlib.ticker as ticker

def data_generator(reader, skip_lines=30):
    skip_counter = skip_lines-1
    for row in reader:

        if skip_counter == 0:
            # Yield the values, assuming `time` is the first column
            yield (float(row[0]), float(row[1]), float(row[2]),
                    float(row[3]), float(row[4]))
            skip_counter = skip_lines - 1
            
        else:
            skip_counter -= 1

    file.seek(0)
    data_generator(reader, skip_lines)


limit = 1e9
skip_lines = 30
const_fps = 60
interval = 1000 / const_fps

with open("Newton.csv", "r") as file:
    reader = csv.reader(file)

    # Initialize plot
    fig, ax = plt.subplots()
    body1, = ax.plot([], [], 'bo', label='Body 1')  # Blue circle for Body 1
    body2, = ax.plot([], [], 'ro', label='Body 2')  # Red circle for Body 2
    ax.legend()

    # Set plot limits (adjusted for the 10^9 scaling factor)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    # Enable grid and set up major and minor ticks
    ax.grid(True)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/limit*100:.0f}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y/limit*100:.0f}'))

    # Display text for simulation time
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        body1.set_data([], [])
        body2.set_data([], [])
        time_text.set_text('')
        return body1, body2, time_text

    def update(frame):

        current_data = next(data_generator(reader, int(fps_slider.val)))

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
    fps_slider = Slider(slider_ax, "skip_lines", 1, 10000, valinit=skip_lines, valstep=1)

    # Enable interactive pan/zoom in the plot
    plt.gca().set_aspect('auto', adjustable='box')
    fig.canvas.toolbar_visible = True  # Shows the interactive toolbar with pan and zoom options

    plt.show()
