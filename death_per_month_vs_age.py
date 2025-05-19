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
annual_mortality_rates = []

# Simulate until cohort is nearly depleted
t = 0
while t < max_months and population[-1] >= 100:
    # Age in years
    age = 30 + t / 12
    # Annual mortality rate
    mu_annual = mu_0_annual * np.exp(k * (age - 30))
    annual_mortality_rates.append(mu_annual)
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
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(ages[:-1], deaths, 'b-', label='Monthly Deaths')
ax1.set_title('Monthly Deaths vs Age for Cohort of 100,000 Starting at Age 30')
ax1.set_xlabel('Age (Years)')
ax1.set_ylabel('Number of Deaths per Month')
ax1.grid(True)
ax1.legend(loc='upper right')
ax1.set_xticks(np.arange(30, max(ages), 10))

# Add secondary x-axis for annual mortality rate
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
mortality_tick_ages = np.arange(30, max(ages), 10)
mortality_tick_labels = [f"{(mu_0_annual * np.exp(k * (age - 30)) * 100):.1f}%" for age in mortality_tick_ages]
ax2.set_xticks(mortality_tick_ages)
ax2.set_xticklabels(mortality_tick_labels)
ax2.set_xlabel('Annual Mortality Rate')

# Show and save plot
plt.tight_layout()
plt.show()
# plt.savefig('mortality_vs_age_plot.png')
plt.close()
