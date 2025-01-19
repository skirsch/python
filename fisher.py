#!/bin/python
import scipy
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

# NOTE: scipy uses a more sophisticated formula to estimate the true OR
# when the numbers are small. It computes the maximum likelihood estimate for the odds ratio

# say vaccine is making things worse with more deaths
# argument ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,
# so the OK people first, then the # of injured
# start with NO TREAT

# odds ratio is simply (a/b)/(c/d) which is same as (a/c)/(b/d)

# from the matrix, the odds ratio is multiply the AD axis and divide by the 
# opposite axis

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
    a=round(placebo_ok)
    b=round(treat_ok)
    c=round(placebo_bad)
    d=round(treat_bad)
    print("\nStatistics for", description, "=", a,b,c,d, a+c, b+d, a+b+c+d)
    res=(fisher_exact([[a,b],[c,d]],'greater')) # one-sided p-value
    print("One-sided p-value", res.pvalue)  # probability of seeing at least this many events, given expected of a:c
    res2=(fisher_exact([[a,b],[c,d]],'two-sided')) # one-sided p-value
    print("Two-sided p-value", res2.pvalue)  # probability this is DIFFERENT than control
    res=odds_ratio([[a,b],[c,d]])
    print("Max likelihood estimate of the Odds ratio=", res.statistic)
    if b*c>0:
        print("Traditional OR=", (a*d)/(b*c))
    #print("99.99%", res.confidence_interval(confidence_level=0.9999))  # 99.99% confidence interval
    print("99.9%", res.confidence_interval(confidence_level=0.999))  # 99.9% confidence interval
    print("99%", res.confidence_interval(confidence_level=0.99))  # 99% confidence interval
    print("95%", res.confidence_interval(confidence_level=0.95))  # 95% confidence interval
    print("90%", res.confidence_interval(confidence_level=0.90))  # 95% confidence interval
    #print("85%", res.confidence_interval(confidence_level=0.85))  # 95% confidence interval
    #print("80%", res.confidence_interval(confidence_level=0.80))  # 95% confidence interval
# analyze1 will take total cases as the first two arguments
def analyze1(a,b,c,d,desc):
    analyze(a-c, b-d, c, d, desc)

# placebo total injected, placebo dead, experiment injected, experiment dead
def analyze2(a,c,b,d, desc):
    analyze(a-c, b-d, c, d, desc)

'''
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

# 1955 -1959 (age 65-69)
# pfizer enrolled, moderna enrolled, pfizer dead, moderna dead
analyze1(411920, 39973, 3463, 534, "pfizer vs. moderna study1 ages 65-69")

# Shots given in 1940s Pfizer vs. Novavax 2nd shot in April 2022
analyze(68, 94, 1, 7, "novavax vs. pfizer second shot in apr 2022 to those born in 1940s")

# CT Medicare date for 85-89 year olds
# moderna is the placebo and listed first
analyze1(5786,19264 ,417, 1838, "CT Medicare 85-89 shot 2 1 year shots/deaths")

# Apple Valley
# placebo infected, dead ....; then "treated" infected, dead
# clearly we didn't get unlucky
# in this case, placebo is before vax rolled out 
analyze2(27,0, 90, 28, "apple valley village before vax, after vax")
# unvaxxed #, myo/peri carditis #
# https://www.medrxiv.org/content/10.1101/2024.05.20.24306810v1.full.pdf
analyze2(47837, 0, 47803, 12, "myopericarditis")
analyze2(47837, 0, 47803, 3, "deaths")

### batch analysis
analyze2(40984,179,10746,84, "FD6840 vs FC2473, 60-64 year olds")

### June 2021 administration
# age 60-64 Comirnaty
analyze2(72904,178, 6238,48, "FD0168 v FC2473, age 60-64, June 2021")
# age 50-64
analyze2(138288,296, 16073,102, "FD0168 FC2473 Jun 1, age 50-65")
analyze2(23614, 33, 5025, 22, "FD0168 FC2473 Jun 1, age 50-54")

# FC0681 looks deadly to 60-65
# FC2473
# FF2832
# FF3318
# FA4598

# low impact
# FD0168 FD4555 FE1248

## new zealand batch data
analyze2(14205,70, 2605,40, "NZ 60-64 year olds")

analyze2(3123, 152, 520,54, "85 to 90 year olds dose 3 jan 2022, new zealand batches 34, 39")

analyze2(5520, 139, 3053, 194, "batch 34 vs. batch 38 for ages 80 to 84 given jan feb 2022")
analyze2(235762, 112, 232692, 130, "25-29 v 20-24 new zealand all batches and doses")


analyze2(47837, 0, 47802, 12, "kids with myo/pericarditis in UK study")

### dose 1 pfizer vs moderna in czech study (this is overall numbers)
analyze2(5449647, 51458, 516562, 10018, "Pfizer vs. Moderna Dose 1 czech data")

# child asthma paper   unvaxxed N and deaths, vaxxed N and deaths
analyze2( 159357, 140+169,  32088, 188+166, "asthma paper" )

'''

analyze2(2576, 330, 891,168, "SCC public health LTCF")
analyze2(1000, 13, 1000, 36, "pollfish survey")

# Xie JAMA paper
# # analyze is placebo ok, treat ok
# placebo is flu rates when for looking at COVID vax rates
p=2403 # placebo got flu
t=8996 # treatment

# vaccinated vs. unvaccinated
a=1-.1889  # hospitalized for the flu
b=1-.2073  # hospitalized for COVID (20.73% unvaxxed)
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "vaxxed vs. uvax ")

# with propensity flu changes
a=1-.1784
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "vaxxed vs. uvax with propensity ")

# benefit of booster
a=.5485
b=.5454
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "booster only benefit")

############## propensity stuff

# benefit of dose 1 shot
a=.0468  # flu rate
b=.0427  # Covid rate
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "dose 1 only with propensity")

# benefit of dose 2 shot
a=.2206  # flu rate
b=.2047  # Covid rate
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "primary series benefit with propensity")

# benefit of being fully vaccinated (booster) propensity
a=.5543  # flu rate
b=.5454  # Covid rate
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "boosted benefit with propensity")

#################################
# now for 1 dose
a=.0474
b=.0427
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "1 dose only")

# 1 and 2 doses
a=a+.2151 # control flu rate
b=b+.2046
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "both primary doses ")

# need to take 3 doses to get a benefit and it's not statistically significant

### I screwed up. and reversed the args for the paper!
# flu
a=.6384   # control vaxxed covid rate
b=.6188   # treatment vaxxed flu rate
t=2403 # treatment got flu
p=8996 # placebo COVID rate
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "flu vaccine before propensity")
analyze((1-a)*p, (1-b)*t, a*p, b*t, "flu vaccine before propensity")


a=.6384   # control vaxxed covid rate
b=.6343   # treatment vaxxed flu rate
t=2403 # treatment got flu
p=8996 # placebo COVID rate
analyze(a*p, b*t, (1-a)*p, (1-b)*t, "flu vaccine after propensity")

### rct
analyze(22000, 14, 22000, 15, "pfizer rct")

### santa clara county CFR by quarter with 8 day death shift
analyze2(3749,409, 1020, 244, "scc phd CFR Q4 vs. Q1")

### Paul Thomas study... no vax injected, cases ; full vaxxed 
analyze2(561, 0, 894, 15, "paul thomas autism study")

# Pfizer preg clinical trial
# vs. 159 2 events (placebo) vs 156, 8  drugged 
analyze2(159,2, 156,8, "Pfizer preg trial outcome 19")

# frontiers COVID paper
# unvaxxed total, unvaxxed die, vaxxed total, vaxxed died
analyze2(89, 89*.37, 23, 23*.7, "Frontiers Adhikari paper; Odds of dying from COVID if you were vaccinated")


# same calculation but look at those who died from non-COVID
# 25 unvaxxed, 36% died. 15 vaxxed, 27% died
analyze2(25, .36*25, 15, 15*.27, "Frontiers; died from non-COVID")

# now reverse the order to see if you were 2x more likely if you were unvax
# so vaxxed is first so OR is the other way
analyze2(15, 15*.27, 25, .36*25, "Frontiers; died from non-COVID")

analyze2( 162,2, 8,1, "pfizer CFR")
analyze2(850,2, 77,1, "pfizer CFR")
# Prison outbreak https://www.cdc.gov/mmwr/volumes/70/wr/mm7038e3.htm
# VE was only 13%3
analyze2(42,3,185,56,  "prison outbreak")
# barnstable 469 cases. 
# control would be 469
# 69% population vaxxed so expected .69*469 to get infected
analyze2(649, int(649*.69), 649, int(649*.74), "barnstable")

# pfizer serropositive
# https://www.medrxiv.org/content/10.1101/2022.04.18.22271936v1.full
# https://philharper.substack.com/p/a-public-verification-of-jikkyleaks?utm_source=publication-search
analyze2(133,40, 160+75, 75, "pfizer N-antibody" )

analyze2(10,1, 75, 75, "office COVID infections")

analyze2(228, 116, 1445, 1420, "infection rate of unv vs vaxxed")

# low vs. high covid cases
analyze(5702, 2394, 714, 228, "covid cases for 9x% vax vs 8x% vax")
analyze(5702, 1660, 714, 166, "9x% vs. 7x%")
# so both are statistically signif lower than the 90%

# but 7x and 8x are similar; no difference; and 8x is worse
analyze(2394, 1660, 228, 166, "8x vs. 7x%") 