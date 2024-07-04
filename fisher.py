#!/bin/python
import scipy
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

# say vaccine is making things worse with more deaths
1623
# argument ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,
# so the OK people first, then the # of injured
# start with NO TREAT

# odds ratio is simply (a/b)/(c/d) which is same as (a/c)/(b/d)

# BEWARE OF the ONE-SIDED p-value!
# the order of arguments matters (unlike for the two sided p-value)
# analyze(100, 100, 1, 10, "80 year olds")
# is your chance of seeing 10 or more events given you expect 1 (rare)

# analyze(100, 100, 10, 1, "80 year olds")
# is the chance you'll see 1 or more events, given you expect to see 
# 10 events (the control). This is almost certain to happen!

# so only use one-sided test when your experiment has HIGHER death rate than the control.
# (because the criteria was "GREATER" in our one-sided testcum)

# this gives a statistic of 10 since odds of damage is 10X greater with the vax
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]]))   # two-sided p-value .01  odds ratio is 10X
# print(scipy.stats.fisher_exact([[10, 100], [1, 100]], 'greater'))  # one-sided p-value if hypothesis of harm only

def analyze(placebo_ok, treat_ok,placebo_bad, treat_bad, description):
    a=placebo_ok
    b=treat_ok
    c=placebo_bad
    d=treat_bad
    print("\nStatistics for", description, "=", a,b,c,d, a+b+c+d)
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

# Gender ratio for different doses
# control is dose 3
# ages 36 to 70 where m:f stats are constant
# 0 to 180 days post dose
# dose 3: 507,377 male:female
# dose 2: 454, 281
analyze(507, 454, 377, 281, "gender ratio test")

# for 40 to 77
# dose 3: 968, 697
# dose 2: 698, 420
# dose 1: 597, 355
# put dose 2 or 1 first
analyze(698,969, 420,697, "gender ratio of 40 to 77 dose 2 vs. 3")
analyze(597,969, 355,697, "gender ratio of 40 to 77 dose 1 vs. 3")
analyze(386, 2435,221, 1662, "gender ratio first 120 days vs. after 120 days dose 1")
analyze(3972,   919, 2691, 907, "dose 4")
analyze(6270, 263,  6699, 397, "aug sept 2021 injection vs. 1 year later NZ")
# compute for NZ OIA request
analyze(94,1662, 103, 1992, "NZ OIA month before peak COVID vs. month of peak COVID")

# See vaccine infection stats.xlsx in OneDrive substack folder for the next 3
# you are 1.24 more likely to get a COVID infection if you were vaccinated
analyze(5226, 575, 11827, 1618, "substack 20,000 covid infection survey")
analyze(1842,629, 3286, 2330, "unvaxxed vs. highly vaxxed risk of getting COVID")
analyze(9778, 259, 7802, 327, "X survey on COVID infections")

# sexual orientation issues for those under 24 years old
analyze(391, 299, 1, 8, "sexual orientation issues those under 24")

# for those under 60
analyze(900,1366, 1, 22, "under 60 sex orientation")

# statistics for No abnormal health conditions
# there were 1745 with no vax and 1623 people highly vaxxed in our
# sample in first 10,000
analyze(1026, 422, 1262, 1794, "no chronic disease")

analyze(2325, 2112, 18, 115, "5 or more chronic conditions")
analyze(6977, 736, 44, 20, "Mom vaccinated during pregnancy vs. birth defects")

analyze(21828-60, 21823-311,60, 311, "Pfizer trial exclusions")

# JAMA study
analyze(2403-1318, 8996-4906, 1318, 4906, "JAMA paper covid vs. flu VA")

# Moderna vs. Pfizer stats on mortality for those born in 1956 (5 year period)
analyze(420903, 43883, 4808,782, "moderna/pfizer mortality numbers")
