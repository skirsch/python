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

# analyze1 will take total cases as the first two arguments
def analyze1(a,b,c,d,desc):
    analyze(a-c, b-d, c, d, desc)

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

# VHA rates
# boosted 238 infected; 4 deaths
# unboosted 739 infected 10 deaths
analyze(729, 234, 10, 4, "VHA boosted/unboosted death from COVID")

# US Nursing home data before/after rollout
# Note this is so large that it won't compute a probab
analyze1(188203, 204890, 31150, 35590, "Nursing home 12 week case")
analyze1(18820, 20489, 3115, 3559, "Nursing home 12 week case") # faster to compute confidence