import math
from scipy.stats import norm

# Inputs: deaths and person-time
# unvaxxed
dA1, tA1 = 1440, 834000
dA2, tA2 = 6883, 3268000

# vaxxed
dB1, tB1 = 3096,   4805000
dB2, tB2 = 23290, 26162000

# Rates
rA1 = dA1 / tA1
rA2 = dA2 / tA2
RR_A = rA2 / rA1

rB1 = dB1 / tB1
rB2 = dB2 / tB2
RR_B = rB2 / rB1

# Log difference and standard error of difference
log_diff = math.log(RR_A) - math.log(RR_B)
SE_diff = math.sqrt(1/dA1 + 1/dA2 + 1/dB1 + 1/dB2)
z = log_diff / SE_diff
p = 2 * (1 - norm.cdf(abs(z)))

# 95% CI for RR_A
SE_A = math.sqrt(1/dA1 + 1/dA2)
ci_A_lower = RR_A * math.exp(-1.96 * SE_A)
ci_A_upper = RR_A * math.exp(1.96 * SE_A)

# 95% CI for RR_B
SE_B = math.sqrt(1/dB1 + 1/dB2)
ci_B_lower = RR_B * math.exp(-1.96 * SE_B)
ci_B_upper = RR_B * math.exp(1.96 * SE_B)

# Output
print(f"RR_A = {RR_A:.4f}, 95% CI: ({ci_A_lower:.4f}, {ci_A_upper:.4f})")
print(f"RR_B = {RR_B:.4f}, 95% CI: ({ci_B_lower:.4f}, {ci_B_upper:.4f})")
print(f"z = {z:.3f}, p-value = {p:.6f}")