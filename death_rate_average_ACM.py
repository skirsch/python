import numpy as np

# Define annual mortality rates for two groups
mortality_group1_annual = 0.09   # Group A
mortality_group2_annual = 0.03   # Group B

# Convert to weekly mortality rates assuming exponential decay (constant hazard)
weeks_per_year = 52
weekly_mortality_group1 = 1 - (1 - mortality_group1_annual) ** (1 / weeks_per_year)
weekly_mortality_group2 = 1 - (1 - mortality_group2_annual) ** (1 / weeks_per_year)

# Simulate for 80 weeks
weeks = np.arange(0, 80)
pop_group1 = [1.0]
pop_group2 = [1.0]
deaths_group1 = []
deaths_group2 = []

# Weekly mortality simulation
for _ in weeks:
    alive_1 = pop_group1[-1]
    alive_2 = pop_group2[-1]

    d1 = alive_1 * weekly_mortality_group1
    d2 = alive_2 * weekly_mortality_group2

    deaths_group1.append(d1)
    deaths_group2.append(d2)

    pop_group1.append(alive_1 - d1)
    pop_group2.append(alive_2 - d2)

# Convert to arrays for calculations
deaths_group1 = np.array(deaths_group1)
deaths_group2 = np.array(deaths_group2)
at_risk_group1 = np.array(pop_group1[:-1])
at_risk_group2 = np.array(pop_group2[:-1])

# Average weekly mortality = total deaths / total person-weeks at risk
avg_weekly_mortality_group1 = deaths_group1.sum() / at_risk_group1.sum()
avg_weekly_mortality_group2 = deaths_group2.sum() / at_risk_group2.sum()

# Annualize
avg_annual_mortality_group1 = avg_weekly_mortality_group1 * weeks_per_year
avg_annual_mortality_group2 = avg_weekly_mortality_group2 * weeks_per_year

# Compute percent increase over baseline annual rate
increase_group1 = (avg_annual_mortality_group1 - mortality_group1_annual) / mortality_group1_annual * 100
increase_group2 = (avg_annual_mortality_group2 - mortality_group2_annual) / mortality_group2_annual * 100

# Results
print(f"Group A - Average Annual Mortality: {avg_annual_mortality_group1:.4%}, Increase: {increase_group1:.2f}%")
print(f"Group B - Average Annual Mortality: {avg_annual_mortality_group2:.4%}, Increase: {increase_group2:.2f}%")
