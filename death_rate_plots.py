import numpy as np
import matplotlib.pyplot as plt

# Mortality rates by age for US males starting at age 70
data = {
    70: 0.022381, 71: 0.024185, 72: 0.026266, 73: 0.028660, 74: 0.031401,
    75: 0.034618, 76: 0.038263, 77: 0.042190, 78: 0.046367, 79: 0.050948,
    80: 0.056237, 81: 0.062360, 82: 0.069226, 83: 0.076884, 84: 0.085452,
    85: 0.095062, 86: 0.105829, 87: 0.117838, 88: 0.131138, 89: 0.145751,
    90: 0.161678, 91: 0.178905, 92: 0.197408, 93: 0.217149, 94: 0.238080,
    95: 0.258821, 96: 0.278966, 97: 0.298092, 98: 0.315762, 99: 0.331550,
    100: 0.348128
}

# Parameters
initial_population = 10000
weeks_per_year = 52

# Prepare weekly simulation over 30 years
total_weeks = 30 * weeks_per_year
weekly_deaths = []
weekly_mortality_rates = []
population = initial_population

# Generate age list for each week
ages = [70 + (w / weeks_per_year) for w in range(total_weeks)]

for week in range(total_weeks):
    age = 70 + week / weeks_per_year
    age_floor = int(np.floor(age))
    age_ceil = min(age_floor + 1, 100)

    # Linear interpolation of mortality rate between integer ages
    weight = age - age_floor
    if age_floor >= 100:
        mortality_rate_annual = data[100]
    else:
        mortality_rate_annual = (1 - weight) * data[age_floor] + weight * data[age_ceil]

    # Convert to weekly rate
    weekly_mortality = 1 - (1 - mortality_rate_annual) ** (1 / weeks_per_year)
    deaths = population * weekly_mortality

    weekly_deaths.append(deaths)
    weekly_mortality_rates.append(weekly_mortality)
    population -= deaths

# Convert weekly mortality rates to annualized for plotting
annualized_mortality_rates = [rate * weeks_per_year for rate in weekly_mortality_rates]

# Plotting
weeks = np.arange(total_weeks)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(weeks, weekly_deaths, label='Weekly Deaths', color='red')
plt.xlabel('Week')
plt.ylabel('Number of Deaths')
plt.title('Weekly Deaths in a Cohort of 10,000 Males (Age 70+)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(weeks, annualized_mortality_rates, label='Annualized Mortality Rate', color='blue')
plt.xlabel('Week')
plt.ylabel('Annualized Mortality Rate')
plt.title('Annualized Mortality Rate Over Time')
plt.grid(True)

plt.tight_layout()
plt.show()
