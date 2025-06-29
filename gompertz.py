import numpy as np
import matplotlib.pyplot as plt

# Define the Gompertz function
def gompertz_curve(t, a, b, c):
    return a * np.exp(-b * np.exp(-c * t))

# Derivative of the Gompertz function to get the rate of new infections
def gompertz_derivative(t, a, b, c):
    return a * b * c * np.exp(-c * t) * np.exp(-b * np.exp(-c * t))

# Parameters for the Gompertz curve
a = 100  # Asymptote, representing the maximum number of infections
b = 5   # Position parameter. Larger value shifts to right
c = 2  # Growth rate parameter. Smaller means slower growth. 5 is a rapid growth

# Generate time points
t = np.linspace(0, 20, 100)
y = gompertz_curve(t, a, b, c)  # Cumulative infections
new_infections = gompertz_derivative(t, a, b, c)  # Rate of new infections

# Plot both the cumulative infections and the rate of new infections
plt.figure(figsize=(12, 8))

# Plot cumulative infections (Gompertz curve)
plt.plot(t, y, label='Cumulative Infections (Gompertz Curve)', color='blue')

# Plot rate of new infections (Gompertz derivative)
plt.plot(t, new_infections, label='New Infections (Rate of Spread)', color='green')

# Labels and title
plt.xlabel('Time')
plt.ylabel('Number of Infections')
plt.title('Gompertz Curve for Viral Spread and New Infections Over Time')
plt.axhline(a, linestyle='--', color='red', label='Asymptote (Maximum Cumulative Infections)')
plt.legend()
plt.grid(True)
plt.show()

