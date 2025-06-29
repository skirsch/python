import matplotlib.pyplot as plt
import numpy as np

# Parameters
months = 24
total_population = 100000
vaccination_rate = 0.7
vaccinated_population = total_population * vaccination_rate
unvaccinated_population = total_population * (1 - vaccination_rate)
annual_mortality_increase = 1.08  # 8% annual increase in mortality
k = np.log(annual_mortality_increase)
monthly_increase = annual_mortality_increase**(1/12)

# Parameterized annual mortality rates (in percentage, e.g., 1 means 1%)
annual_mortality_vaccinated = 1  # Vaccinated: 1% annual mortality
annual_mortality_unvaccinated = 15  # Unvaccinated: 5% annual mortality

# Convert to fractions (e.g., 1% = 0.01)
annual_mortality_vaccinated = annual_mortality_vaccinated / 100
annual_mortality_unvaccinated = annual_mortality_unvaccinated / 100

# Initialize arrays
population_vaccinated = [vaccinated_population]
population_unvaccinated = [unvaccinated_population]
deaths_vaccinated = []
deaths_unvaccinated = []
cumulative_deaths_vaccinated = 0
cumulative_deaths_unvaccinated = 0

# Simulate for 24 months
for t in range(months):
    # Vaccinated
    mu_annual_vaccinated = annual_mortality_vaccinated * (monthly_increase ** t)
    mu_monthly_vaccinated = 1 - (1 - mu_annual_vaccinated)**(1/12)
    deaths = population_vaccinated[-1] * mu_monthly_vaccinated
    deaths_vaccinated.append(deaths)
    cumulative_deaths_vaccinated += deaths
    population_vaccinated.append(population_vaccinated[-1] - deaths)
    
    # Unvaccinated
    mu_annual_unvaccinated = annual_mortality_unvaccinated * (monthly_increase ** t)
    mu_monthly_unvaccinated = 1 - (1 - mu_annual_unvaccinated)**(1/12)
    deaths = population_unvaccinated[-1] * mu_monthly_unvaccinated
    deaths_unvaccinated.append(deaths)
    cumulative_deaths_unvaccinated += deaths
    population_unvaccinated.append(population_unvaccinated[-1] - deaths)

# Calculate ratios
r1 = deaths_vaccinated[0] / deaths_unvaccinated[0] if deaths_unvaccinated[0] != 0 else float('inf')
r2 = cumulative_deaths_vaccinated / cumulative_deaths_unvaccinated if cumulative_deaths_unvaccinated != 0 else float('inf')
r3 = r1 / r2 if r2 != 0 else float('inf')

# Calculate slopes
vaccinated_slope = (deaths_vaccinated[-1] - deaths_vaccinated[0]) / (months - 1)
unvaccinated_slope = (deaths_unvaccinated[-1] - deaths_unvaccinated[0]) / (months - 1)

# Plot 1: Absolute monthly deaths
plt.figure(figsize=(10, 6))
plt.plot(range(1, months + 1), deaths_vaccinated, 'b-', label=f'Vaccinated ({annual_mortality_vaccinated*100}% annual mortality)')
plt.plot(range(1, months + 1), deaths_unvaccinated, 'r-', label=f'Unvaccinated ({annual_mortality_unvaccinated*100}% annual mortality)')
plt.title('Expected Monthly Deaths for Vaccinated and Unvaccinated (2021-2022)')
plt.xlabel('Month (Jan 2021 to Dec 2022)')
plt.ylabel('Number of Deaths per Month')
plt.grid(True)
plt.legend()
plt.xticks(np.arange(1, months + 1, 3))
plt.ylim(0, max(max(deaths_vaccinated), max(deaths_unvaccinated)) * 1.1)  # Dynamic y-axis with 10% padding

# Add text box with r1, r2, r3 and slopes in the lower-left corner
textstr = f'r1 (Jan 2021): {r1:.4f}\n'
textstr += f'r2 (Cumulative): {r2:.4f}\n'
textstr += f'r3 (r1/r2): {r3:.4f}\n'
textstr += f'Vaccinated Slope: {vaccinated_slope:.2f} deaths/month\n'
textstr += f'Unvaccinated Slope: {unvaccinated_slope:.2f} deaths/month'
plt.text(0.05, 0.05, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='bottom', horizontalalignment='left',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Save the first plot
plt.show()
# plt.savefig('absolute_mortality_2021_2022_mortality_rates.png')
plt.close()

# Plot 2: Relative change in monthly deaths (normalized to starting value)
relative_deaths_vaccinated = [d / deaths_vaccinated[0] for d in deaths_vaccinated]
relative_deaths_unvaccinated = [d / deaths_unvaccinated[0] for d in deaths_unvaccinated]

plt.figure(figsize=(10, 6))
plt.plot(range(1, months + 1), relative_deaths_vaccinated, 'b-', label=f'Vaccinated ({annual_mortality_vaccinated*100}% annual mortality)')
plt.plot(range(1, months + 1), relative_deaths_unvaccinated, 'r-', label=f'Unvaccinated ({annual_mortality_unvaccinated*100}% annual mortality)')
plt.title('Relative Change in Monthly Deaths (Normalized to Jan 2021)')
plt.xlabel('Month (Jan 2021 to Dec 2022)')
plt.ylabel('Relative Deaths (Jan 2021 = 1)')
plt.grid(True)
plt.legend()
plt.xticks(np.arange(1, months + 1, 3))
plt.ylim(0, 2)  # Y-axis from 0 to 2 as specified
plt.margins(y=0.1)  # Add 10% margin above and below the data

# Save the second plot
plt.show()
# plt.savefig('relative_mortality_2021_2022_mortality_rates.png')
plt.close()