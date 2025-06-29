import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Time range
t = np.linspace(-10, 10, 100)

# Parameters for normal distribution
mu = 0
sigma = 2
scale_daily = 0.2 * np.sqrt(2 * np.pi * sigma**2)  # Scale to match peak of 0.2

# Original daily deaths (normal distribution)
daily_deaths = (1 / np.sqrt(2 * np.pi * sigma**2)) * np.exp(-(t - mu)**2 / (2 * sigma**2)) * scale_daily

# Original cumulative deaths (numerical integration of daily deaths)
cum_deaths = np.cumsum(daily_deaths) * (t[1] - t[0])

# Vaccine coverage: linear from t = -2.5 to t = 2.5
coverage = np.zeros_like(t)
for i in range(len(t)):
    if t[i] < -2.5:
        coverage[i] = 0
    elif t[i] <= 2.5:
        coverage[i] = (t[i] + 2.5) / 5
    else:
        coverage[i] = 1

# Vaccine effectiveness: 99%
effectiveness = 0.99

# Adjusted daily deaths
adjusted_daily_deaths = daily_deaths * (1 - effectiveness * coverage)

# Adjusted cumulative deaths (numerical integration, no scaling)
adjusted_cum_deaths = np.cumsum(adjusted_daily_deaths) * (t[1] - t[0])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, daily_deaths, 'y-', label='Original Daily Deaths')
plt.plot(t, adjusted_daily_deaths, 'g-', label='Adjusted Daily Deaths (w/ Vaccine)')
plt.plot(t, cum_deaths, 'r--', label='Original Cumulative Deaths')
plt.plot(t, adjusted_cum_deaths, 'm--', label='Adjusted Cumulative Deaths (w/ Vaccine)')
plt.xlabel('Time')
plt.ylabel('Deaths')
plt.title('Vaccine Impact: 99% Effective, 100% Coverage by t = 2.5, Rollout from t = -2.5')
plt.legend()
plt.grid(True)
plt.show()
