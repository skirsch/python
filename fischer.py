#!/bin/python
import scipy
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

# say vaccine is making things worse with more deaths
# argument ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,
# so the OK people first, then the # of injured


# this gives a statistic of 10 since odds of damage is 10X greater with the vax
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]]))   # two-sided p-value .01  odds ratio is 10X
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]], 'greater'))  # one-sided p-value if hypothesis of harm only

def analyze(a,b,c,d, description):
    print("\nStatistics for", description, a,b,c,d)
    res=(fisher_exact([[a,b],[c,d]],'greater')) # one-sided p-value
    print("One-sided p-value", res.pvalue)
    res=odds_ratio([[a,b],[c,d]])
    print("Odds ratio=", res.statistic)
    print(res.confidence_interval(confidence_level=0.95))  # 95% confidence interval

analyze(50,143,0,7, "wayne root deaths")
analyze(50,117,0,33, "wayne root injuries")
analyze(50, 750, 0, 250, "podiatrist")
analyze(1875, 5605,0, 20, "jay bonnar injuries" )
analyze(1875, 5610,0, 15, "jay bonnar deaths" ) 
analyze(999999, 561000,1, 15, "jay bonnar deaths with 750,000 friends vs. CDC rate" ) 
analyze(999999, 14000,1, 15, "jay bonnar deaths per dose vs. FDA claims")
analyze(999999, 140000,1, 15, "jay bonnar deaths per dose vs. FDA claims assuming he has 75K friends")
analyze(999999, 14000,1, 4, "jay bonnar same-day deaths per dose vs. FDA claims")
analyze(999999, 100,1, 3, "my genesis story: 3 relatives who died post jab")

# ths is from the nursing home dataset comparing
# the week ending 12/6/20 vs. week ending 2/28/21 numbers
# analyze(511163, 90467, 21952, 6117, "IFR")

# 12/6 vs 2/28
# 12/6 4808 deaths on 26525 cases control
# 2/28 621 deaths on 2077 cases
analyze(26525-4808, 2077-621, 4808, 621, "Nursing home 12/6 vs. 2/28 with one week offset")



# VHA rates
# boosted 238 infected; 4 deaths
# unboosted 739 infected 10 deaths
analyze(729, 234, 10, 4, "VHA boosted/unboosted death from COVID")
