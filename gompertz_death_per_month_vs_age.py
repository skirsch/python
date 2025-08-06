# gompertz mortality model simulation and visualization WITH frailty

# This script simulates the Gompertz mortality model for a cohort of 100,000 individuals starting at specified age (70 or 30).
# It calculates the number of deaths per month based on the Gompertz model parameters and frailty factor.
# it shows the number of deaths per month as a function of age, and the annual mortality rate on a secondary x-axis.

import matplotlib.pyplot as plt
import numpy as np

# Frailty parameter (scalar multiplier)
# # Set to 1.0 for no frailty, >1 for higher risk, <1 for lower risk
# Example: frailty = 4 means the mortality rate is 4 times higher than the baseline
# Example: frailty = 0.5 means the mortality rate is half of the baseline (people will live longer)
frailty = .2 # Set to 1.0 for no frailty, >1 for higher risk, <1 for lower risk

# Parameters for Gompertz model
initial_population = 100000
starting_age = 70  # Starting age for the cohort

# use the correct value for the starting age
mu_0_annual = 0.001  # Annual mortality at starting age 30 (this gets the peak at age 86)
mu_0_annual = 0.027  # Annual mortality at starting age 70

# k is the rate of increase in mortality with age
k = np.log(1.08)  # 8% annual increase
max_months = 1200  # 100 years (age 30 to 130)



# Build ages array for the full simulation period
ages = [starting_age + t / 12 for t in range(max_months)]

# Ensure ages array covers at least up to 110
if ages[-1] < 110:
    extra_months = int((110 - ages[-1]) * 12)
    ages += [ages[-1] + (i + 1) / 12 for i in range(extra_months)]

# Simulate deaths per month WITHOUT frailty
population_no_frailty = initial_population
deaths_no_frailty = []
for age in ages:
    mu_annual = mu_0_annual * np.exp(k * (age - starting_age))
    mu_monthly = 1 - np.exp(-mu_annual / 12)
    deaths_t = population_no_frailty * mu_monthly if population_no_frailty > 0 else 0
    if abs(age - 80) < 1e-6:
        print(f"[No Frailty] Age: {age}, Population: {population_no_frailty:.0f}, Annual Mortality: {mu_annual:.4f}, Monthly Prob: {mu_monthly:.4f}, Deaths: {deaths_t:.0f}")
    deaths_no_frailty.append(deaths_t)
    population_no_frailty = max(population_no_frailty - deaths_t, 0)

# Simulate deaths per month WITH frailty
population_frailty = initial_population
deaths_frailty = []
for age in ages:
    mu_annual = frailty * mu_0_annual * np.exp(k * (age - starting_age))
    mu_monthly = 1 - np.exp(-mu_annual / 12)
    deaths_t = population_frailty * mu_monthly if population_frailty > 0 else 0
    if abs(age - 80) < 1e-6:
        print(f"[Frailty] Age: {age}, Population: {population_frailty:.0f}, Annual Mortality: {mu_annual:.4f}, Monthly Prob: {mu_monthly:.4f}, Deaths: {deaths_t:.0f}")
    deaths_frailty.append(deaths_t)
    population_frailty = max(population_frailty - deaths_t, 0)

# Truncate ages to the shortest deaths array
min_len = min(len(deaths_no_frailty), len(deaths_frailty))
ages_plot = ages[:min_len]
deaths_no_frailty = deaths_no_frailty[:min_len]
deaths_frailty = deaths_frailty[:min_len]


# Create the plot

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(ages_plot, deaths_no_frailty, 'b-', label='Monthly Deaths (No Frailty)')
ax1.plot(ages_plot, deaths_frailty, 'r--', label=f'Monthly Deaths (Frailty={frailty:.2f})')
ax1.set_title(f'Monthly Deaths vs Age for Cohort of {initial_population:,} Starting at Age {starting_age}')
ax1.set_xlabel('Age (Years)')
ax1.set_ylabel('Number of Deaths per Month')
ax1.grid(True)
ax1.legend(loc='upper right')
ax1.set_xticks(np.arange(starting_age, 111, 10))

# Add secondary x-axis for annual mortality rate
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
mortality_tick_ages = np.arange(starting_age, 111, 10)
mortality_tick_labels = [f"{(mu_0_annual * np.exp(k * (age - starting_age)) * 100):.1f}%" for age in mortality_tick_ages]
ax2.set_xticks(mortality_tick_ages)
ax2.set_xticklabels(mortality_tick_labels)
ax2.set_xlabel('Annual Mortality Rate')

# Show and save plot
plt.tight_layout()
plt.show()
# plt.savefig('mortality_vs_age_plot.png')
plt.close()

