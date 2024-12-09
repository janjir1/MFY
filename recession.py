import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# Read CSV file
df = pd.read_csv(r'mercury_1e9s\GR.csv')

# Initialize lists to store the zero crossing index and corresponding values
zero_crossings = []
y_values = []

# Iterate over the rows and check for crossings of zero from below
for i in range(1, len(df)):
    if df.iloc[i-1, 2] < 0 and df.iloc[i, 2] >= 0:  # Zero crossing from below
        zero_crossings.append(i)  # Store the index of zero crossing
        y_values.append(df.iloc[i, 1])  # Store the corresponding value from the second column

y_values = [y - 46e9 for y in y_values]

# Create figure and axes
fig, axs = plt.subplots(2, 1, figsize=(10, 10))  # 2 rows, 1 column of subplots

# First plot: Zero crossings and corresponding values from 2nd column
axs[0].plot(zero_crossings, y_values, linestyle='-', color='b')
axs[0].set_xlabel('Number of Zero Passes')
axs[0].set_ylabel('Adjusted Values from 2nd Column at Zero Crossing')
axs[0].set_title('Zero Crossings and Corresponding Adjusted Values from 2nd Column')
axs[0].grid(True)

# Second plot: 3rd column vs 1st column
axs[1].plot(df.iloc[:, 0], df.iloc[:, 2], linestyle='-', color='r')
axs[1].set_xlabel('Values from 1st Column')
axs[1].set_ylabel('Values from 3rd Column')
axs[1].set_title('3rd Column vs 1st Column')
axs[1].grid(True)

# Setup the formatter for both y axes
formatter = EngFormatter(places=1, sep="", unit="m")
axs[0].yaxis.set_major_formatter(formatter)
axs[1].yaxis.set_major_formatter(formatter)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()