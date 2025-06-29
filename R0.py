import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# SIR Model Differential Equations
def sir_model(y, t, R0, gamma):
    S, I, R = y
    beta = R0 * gamma
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Parameters
N = 1.0  # Total population (normalized to 1)
I0 = 0.01  # Initial infected fraction
R0_values = [2.5, 5, 10, 20]  # Different R0 values
gamma = 1/10  # Recovery rate (assuming avg infection duration of 10 days)
S0 = N - I0  # Initial susceptible fraction

# Time grid
t = np.linspace(0, 100, 500)  # 100 days simulation

# Create the plot
plt.figure(figsize=(10, 6))

# Colors for different R0 values
colors = ['blue', 'green', 'orange', 'red']

for i, R0 in enumerate(R0_values):
    y0 = [S0, I0, 0]  # Initial conditions: S, I, R
    solution = odeint(sir_model, y0, t, args=(R0, gamma))
    S, I, R = solution.T  # Extract solutions
    plt.plot(t, I, label=f'R0 = {R0}', color=colors[i])

# Formatting the plot
plt.xlabel('Time (days)')
plt.ylabel('Fraction of Population Infected')
plt.title('Infection Curves for Different R0 Values')
plt.legend()
plt.grid()

# Show the plot
plt.show()
