import numpy as np

# Parameters
cohort_size = 100000  # Starting cohort size at age 30
m0 = 0.0001  # Annual mortality rate at age 30 (0.01%)
k = 0.108  # Adjusted to align peak at age 86 with ~4% annual mortality

# Function to compute annual mortality rate at a given age
def annual_mortality_rate(age):
    return m0 * np.exp(k * (age - 30))

# Compute surviving cohort and monthly deaths from age 30 to 150
ages = np.arange(30, 150.1, 0.1)  # Ages from 30 to 150 in 0.1 increments
surviving = [cohort_size]  # Surviving cohort at each age
monthly_deaths_list = []
annual_mortality_rates = []

for i in range(1, len(ages)):
    age = ages[i]
    m_prev = annual_mortality_rate(ages[i-1])
    survival_prob = (1 - m_prev) ** 0.1
    surviving.append(surviving[-1] * survival_prob)
    m_current = annual_mortality_rate(age)
    monthly_deaths = surviving[-1] * (m_current / 12)
    monthly_deaths_list.append(monthly_deaths)
    annual_mortality_rates.append(m_current * 100)

# Compute slopes using central difference
slopes = []
delta = 0.1
for i in range(len(ages)):
    if i == 0 or i == len(ages) - 1:
        slopes.append(0)
    else:
        slope = (monthly_deaths_list[i] - monthly_deaths_list[i-2]) / (2 * delta)
        slopes.append(slope)

# Compute relative slopes
relative_slopes = []
for i in range(len(ages)):
    if monthly_deaths_list[i] > 0:
        rel_slope = (slopes[i] / monthly_deaths_list[i]) * 100
    else:
        rel_slope = 0
    relative_slopes.append(rel_slope)

# Find the peak
peak_index = np.argmax(monthly_deaths_list)
peak_age = ages[peak_index]
peak_deaths = monthly_deaths_list[peak_index]
peak_mortality = annual_mortality_rates[peak_index]

# Generate table for mortality rates from 0.1% to 25%
results = []
for rate in np.arange(0.001, 0.251, 0.001):  # 0.1% to 25% in 0.1% increments
    idx = np.argmin(np.abs(np.array(annual_mortality_rates) - rate * 100))
    age = ages[idx]
    deaths = monthly_deaths_list[idx]
    slope = slopes[idx]
    rel_slope = relative_slopes[idx]
    results.append((rate * 100, age, deaths, slope, rel_slope))

# Create the complete markdown table
markdown_table = "# Final Corrected Slopes of Mortality Curve at Various Annual Mortality Rates\n\n"
markdown_table += "| Annual Mortality Rate (%) | Age (years) | Monthly Deaths | Slope (deaths/month/year) | Relative Slope (%/year) |\n"
markdown_table += "|--------------------------|-------------|----------------|---------------------------|-------------------------|\n"
for rate, age, deaths, slope, rel_slope in results:
    if (rate <= 10 and rate % 0.5 == 0) or (rate > 10 and rate % 1 == 0):
        markdown_table += f"| {rate:.1f} | {age:.1f} | {deaths:.1f} | {slope:.1f} | {rel_slope:.2f} |\n"

# Print the complete table
print(markdown_table)

# Check the length
print(f"Length of markdown_table: {len(markdown_table)}")
