import matplotlib.pyplot as plt
import numpy as np

# Parameters
initial_population = 100000
mu_0_annual = 0.001  # Annual mortality at age 30
k = np.log(1.08)  # 8% annual increase
max_months = 1200  # 100 years (age 30 to 130)

# Initialize arrays
population = [initial_population]
deaths = []
ages = [30.0]

# Simulate until cohort is nearly depleted
t = 0
while t < max_months and population[-1] >= 100:
    # Age in years
    age = 30 + t / 12
    # Annual mortality rate
    mu_annual = mu_0_annual * np.exp(k * (age - 30))
    # Monthly mortality rate
    mu_monthly = 1 - (1 - mu_annual)**(1/12)
    # Deaths
    deaths_t = population[-1] * mu_monthly
    deaths.append(deaths_t)
    # Update population
    population.append(population[-1] - deaths_t)
    ages.append(age)
    t += 1

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(ages[:-1], deaths, 'b-', label='Monthly Deaths')
plt.title('Monthly Deaths vs Age for Cohort of 100,000 Starting at Age 30')
plt.xlabel('Age (Years)')
plt.ylabel('Number of Deaths per Month')
plt.grid(True)
plt.legend()
plt.xticks(np.arange(30, max(ages) + 1, 10))
# show it
plt.show()
# Save the plot
# plt.savefig('mortality_vs_age_plot.png')
plt.close()
