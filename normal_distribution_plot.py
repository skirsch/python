import numpy as np
import matplotlib.pyplot as plt

# Generate 10,000 points from a normal distribution centered at 0 with a std deviation of 1

N=60

# normal distribution at 0 with std deviation of 1
data = np.random.normal(loc=0, scale=1, size=N)

# Define the new bucket edges with two additional buckets on each tail
# basically, for 3 or more std deviations, there are few data points
# buckets = [-np.inf, -4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, np.inf]
buckets = [-np.inf, -4.25, -3.75, -3.25, -2.75, -2.25, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, np.inf]

# Plot the histogram
plt.hist(data, bins=buckets, edgecolor='black', rwidth=0.8)

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title(f'Histogram of {N} points from a normal distribution')

# Show the plot 
plt.show()
