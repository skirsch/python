#!/bin/python
import scipy
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

# say vaccine is making things worse with more deaths
# ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,

# this gives a statistic of 10 since odds of damage is 10X greater with the vax
print(scipy.stats.fisher_exact([[10, 100], [1, 100]]))   # two-sided p-value .01  odds ratio is 10X
print(scipy.stats.fisher_exact([[10, 100], [1, 100]], 'greater'))  # one-sided p-value if hypothesis of harm only

def analyze(a,b,c,d, description):
    print("\nStatistics for", description, a,b,c,d)
    res=(fisher_exact([[a,b],[c,d]],'greater')) # one-sided p-value
    print("One-sided pvalue", res.pvalue)
    res=odds_ratio([[a,b],[c,d]])
    print("Odds ratio=", res.statistic)
    print(res.confidence_interval(confidence_level=0.95))

analyze(50,143,0,7, "wayne root deaths")
analyze(50,117,0,33, "wayne root injuries")
analyze(50, 750, 0, 250, "podiatrist")
analyze(1875, 5605,0, 20, "jay bonnar injuries" )
analyze(1875, 5610,0, 15, "jay bonnar deaths" )