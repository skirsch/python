# from chatgpt
import statsmodels.api as sm
import scipy.stats as stats
from math import log, exp, sqrt

def calculate_odds_ratio_ci_z_p(a, b, c, d, alpha=0.05):
    # Create a 2x2 contingency table
    table = [[a, b], [c, d]]
    
    # Calculate odds ratio, confidence intervals, z-score, and p-value
    result = sm.stats.Table2x2(table)
    odds_ratio = result.oddsratio
    
    ci_low, ci_high = result.oddsratio_confint(alpha=alpha)

        # Calculate z-score and p-value
    odds_ratio, p_value = stats.fisher_exact(table)
    # calc z score which is (log odds ratio) / SE
    z_score = result.log_oddsratio/result.log_oddsratio_se
    
    
    return odds_ratio, (ci_low, ci_high), z_score, p_value
    
    
# for vaccine in nursing homes on 2/28/21 vs. 12/6/20
c = 4808      # dead unvaxxed
d = 621     # dead vaxxed (exposed; bad outcome)
a = 30894-c    # alive unvax = total unvaxxed - dead
b = 1567-d    # alive vaxxed = total vaxxed participants - dead

# use this function if give as 
# good(control), good(experiment), dead(control), dead(experiment)
# where good means a favorable outcome, e.g., healthy, e.g., got 0 covid infections
def odds(a,b,c,d):
    odds_ratio, confidence_interval, z_score, p_value = calculate_odds_ratio_ci_z_p(a, b, c, d)

    print("Odds Ratio:", odds_ratio)
    print("Confidence Interval:", confidence_interval)
    print("Z-Score:", z_score)
    print("Exact P-Value from Fisher test:", p_value)
    # note that the p-value estimated from the Z-score will be LESS accurate
    # because it assumes a normal distribution
    return odds_ratio

# use odds2 if have TOTAL count unvaxxed, TOTAL count vaxxed, unvaxxed dead, vaxxed dead
# ie., shots, deaths, shots, deahts for placebo then treatment
def odds2(a,b,c,d):
    print("odds before", c/(a-c))
    print("odds after", d/(b-d))
    return (odds(a-c, b-d, c,d))

odds(a,b,c,d)  # compute for our test case

# 8 value odds.. placebo values first
# this is like odds2 but different order: shots, death, then shots,death
# pfizer male (shots, dead) then , pfizer female .then.. moderna same 4 values
def odds8(a,b,c,d,e,f,g,h):
    OR1=odds2(a,c,b,d)
    OR2=odds2(e,g, f,h)
    OR3=OR2/OR1
    print("OR values=", OR1, OR2, OR3)
    print("Confidence interval for", OR3)
    selog=sqrt(1/b+1/d+1/f +1/h)
    or_low = exp(log(OR3)-1.96*selog)
    or_high = exp(log(OR3)+1.96*selog)
    print(or_low, or_high)

    # now confidence interval

# pfizer female, pfizer male (shots, dead)..then.. moderna same 4 values
odds8(212021,	422, 212244,	918,    19218,	47, 18419,	149)

"""
odds2(100,100, 10, 1) gives:

Odds Ratio: 0.09090909090909091
Confidence Interval: (0.011410191847195226, 0.7243053333891898)
Z-Score: -2.264572970885368
P-Value: 0.009658115943518335

Except p-value from Z-score for two-tailed is .0235 and is .011772
for one-tailed
"""

odds(26525-4808, 2077-621, 4808, 621) #  "Nursing home 12/6 vs. 2/28 with one week offset")
# now look at nursing homes getting worse vs. better
odds2(7500, 7500, 169, 1126) # nursing home 2X effect or more

odds(27,62, 0, 28)    # odds ratio for AVV 28,0   90, 28

# ECH covid hospitalization vs. fatality
# note that manual OR will only equal if all integers
odds2(265,663,10,40)


# JAMA propensity numbers
# for COVID vaccine
# unboosted flu, unboosted COVID, boosted flu, boosted covid, 
odds2(2403, 8996, 1332,4906)
odds2(2403, 8996, 1318, 4906)

# for the flu vaccine
# total covid, total flu, got vax covid, got vax flu
odds2(8996, 2403, 5743, 1524)

# for my survey (extended family)
odds2(34270, 34270, 201, 483)
odds2(4000,4000,27, 36)
odds2(40000,40000,368+2*57, 1010+2*299) 
