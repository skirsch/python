import numpy as np

# Assuming the image data is extracted as a string
march = "1.35  1.54  1.43  1.10  1.59  1.44  1.39  1.27  1.13  1.10  1.29  1.11  1.14  1.32  1.38  1.39  1.17  1.10  1.23  1.22  1.36  1.31"
aug = "0.00 0.95 1.87 1.50 1.04 0.54 1.08 0.77 0.79 1.87 0.80 1.05 0.94 1.13 0.70 1.71 1.80"

jan="1.98 1.70 2.69 2.58 1.78 2.38 1.92 2.38 2.40 2.85 2.52 2.34 1.85 2.42 2.29 2.37 2.14 1.86 2.41 3.21 2.79 2.40 2.07 2.61"
feb="1.45 1.52 1.22 1.23 1.56 1.18 1.32 1.48 1.27 1.20 1.24 1.25 1.06 1.36 1.62 1.51 1.05 1.22 1.27 1.36 1.21 1.18 1.44"
mar="1.35 1.54 1.43 1.10 1.59 1.44 1.39 1.27 1.13 1.10 1.29 1.11 1.14 1.32 1.38 1.39 1.17 1.10 1.23 1.22 1.36 1.31"
apr="1.17 1.42 1.23 1.26 1.13 1.28 1.23 1.13 1.11 1.40 1.34 1.34 1.29 1.17 1.28 1.18 1.21 1.16 1.19 1.37 1.24"
may="1.29 1.58 1.88 1.23 1.78 1.77 1.41 1.62 1.67 1.63 1.57 1.39 1.83 1.27 1.60 1.58 1.57 1.70 1.51 1.60"
jun="1.58 1.63 1.75 1.48 1.57 1.23 1.31 1.18 1.51 1.28 1.55 1.57 1.53 1.73 1.45 1.54 1.35 1.58 1.85"
jul="0.64 1.07 1.72 1.52 0.88 1.18 0.77 1.52 1.17 1.72 0.83 1.08 1.20 1.89 1.75 1.54 1.83 1.69"
aug="0.00 0.95 1.87 1.50 1.04 0.54 1.08 0.77 0.79 1.87 0.80 1.05 0.94 1.13 0.70 1.71 1.80"
def stats(numstring, month):
    # Split the string into a list of numbers
    data_list = numstring.split()

    # Convert the list of strings to a numpy array of floats
    data_array = np.array(data_list, dtype=float)

    # Calculate the mean and standard deviation
    mean_value = np.mean(data_array)
    std_deviation = np.std(data_array)
    print(f"Month {month}: mean={mean_value:.4f} std dev={std_deviation:.4f}")
          

month=1
for i in (jan, feb, mar, apr, may, jun, jul, aug):
    stats(i,month)
    month+=1