import numpy as np
import matplotlib.pyplot as plt

"""
# Constants
B = 0.008  # Baseline ACM (0.8%)

# Define Pfizer ACM increase over baseline (%)
pfizer_acm_increase_pct = np.linspace(0.01, 0.8, 500)  # 1% to 80% increase over baseline
P_vals = B * (1 + pfizer_acm_increase_pct)             # Pfizer ACM values
M_vals = 1.2 * P_vals                                  # Moderna is 20% more deadly than Pfizer

# Compute VAERS Moderna:Pfizer ratio
VAERS_ratios = (M_vals - B) / (P_vals - B)
""" 
### mew code assuming Moderna is 20% mortality over baseline fixed (conservative)
B = 0.008
M = 0.0096  # Fixed Moderna ACM = 20% over baseline
P_vals = B * (1 + pfizer_acm_increase_pct)
VAERS_ratios = (M - B) / (P_vals - B)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(pfizer_acm_increase_pct * 100, VAERS_ratios, label='VAERS Ratio (Moderna : Pfizer)')
plt.axhline(y=1.4, color='gray', linestyle='--', label='Target VAERS Ratio (1.4)')
plt.axvline(x=14.3, color='red', linestyle='--', label='Pfizer ACM = 14.3% over baseline')
plt.title('VAERS Moderna:Pfizer Ratio vs. Pfizer ACM Increase Over Baseline')
plt.xlabel('Pfizer ACM Increase Over Baseline (%)')
plt.ylabel('VAERS Report Ratio (Moderna : Pfizer)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
