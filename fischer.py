#!/bin/python
import scipy
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

# BEWARE OF the ONE-SIDED p-value!
# the order of arguments matters (unlike for the two sided p-value)
# analyze(100, 100, 1, 10, "80 year olds")
# is your chance of seeing 10 or more events given you expect 1 (rare)

# analyze(100, 100, 10, 1, "80 year olds")
# is the chance you'll 1 or more events, given you expect to see 
# 10 events (the control). This is almost certain to happen!

# so only use one-sided test when your experiment has HIGHER death rate than the control.
# (because the criteria was "GREATER" in our one-sided test)

# say vaccine is making things worse with more deaths
# argument ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,
# so the OK people first, then the # of injured


# this gives a statistic of 10 since odds of damage is 10X greater with the vax
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]]))   # two-sided p-value .01  odds ratio is 10X
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]], 'greater'))  # one-sided p-value if hypothesis of harm only

def analyze(a,b,c,d, description):
    print("\nStatistics for", description, a,b,c,d, a+b+c+d)
    res=(fisher_exact([[a,b],[c,d]],'greater')) # one-sided p-value
    print("One-sided p-value", res.pvalue)  # probability of seeing at least this many events, given expected of a:c
    res2=(fisher_exact([[a,b],[c,d]],'two-sided')) # one-sided p-value
    print("Two-sided p-value", res2.pvalue)  # probability this is DIFFERENT than control
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

#actual value is first one, but this is time consuming to compute
# analyze1(188203, 204890, 31150, 35590, "Nursing home 12 week case") 
# analyze1(18820, 20489, 3115, 3559, "Nursing home 12 week case") # faster to compute confidence

# JAMA paper on nursing homes
# https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2799266
# System 2 included 128 VHA CLCs; among 
# 3289 boosted residents (3157 [96.0%] male; 1950 [59.3%] White) vs 
# 4317 unboosted residents 
# (4151 [96.2%] male; 2434 [56.4%] White), the median age was 74 (IQR, 70-80) vs 74 (IQR, 69-80) years. 
# A total of 45 SARS-CoV-2–associated deaths occurred in system 1 and 18 deaths occurred in system 2. 
# Per table:
# boosted deaths were 1.3*3.289=4.3
# unboosted deaths were 2.4*4.317=10.4
# from the chart, we have boosted deaths per 1K are 98/158*2 (1.24) 
# and unboosted deaths are 28/158*2+2 = 2.3 which are close to the Table values
# so just go with the table values for now.
# shows a benefit based on population
analyze1(4317, 3289, 10, 4, "jama paper unbboosted v boosted deaths based on number of participants")
# but now lets look at based on # of infections
analyze1(int(4.317*171.2), int(3.289*72.5), 10, 4, "jama paper unbboosted v boosted deaths based on number of infections")
# if just look at the numbers in the table (per 1K), get:
# 
# (Table 3) says that there was a CFR for the System 2 unboosted of  2.4/171.2=.014 per 1K residents. 
# But for the boosted, the case fatality rate was higher at 1.3/72.5=.0179. 
# So it was 28% higher CFR for the boosted. 

# Died suddenly stats
analyze(22,  71-22, 95-22, (506-95)-(71-22), "died normally unvax vs. vax")

