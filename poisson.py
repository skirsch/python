'''
from norman fenton
It's a very different way of looking at the problem 
because you are equating death of a vaxxed person 
as an unexpected death. But if the answer to your 
question is not 1/20 to the power 15. 
You need the Poisson distribution to calculate the 
probability of seeing 15 deathes during a period where 
the probability of seeing one is 1/20 (=0.05). Specifically 
the formula is this where e is the constant  
lambda is 0.05 and k=15. 
The result is essentially 0 but strictly 
speaking we want to know P(X >=k) but that is also 
essentially 0
'''

# Survival function (also defined as 1 - cdf, but sf is sometimes more accurate).

# reference manual here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html
# chance of getting K events where you expect l chance 
# of getting an event in the period
# so k=15, l=.1 where 1/10 chance of getting one event
# # since tail is very small, if you compute value for say 15 events and expecting 1, 
# cum probab in tail is at most double that value


#  
import math
from scipy.stats import poisson
# chance of getting exactly k events when expect l events

# poisson.cdf(0,15) means you got 0 or less events and expected 15
def p(k,l):
    return poisson.pmf(k,l)    # this works always. point value.
    # use .cdf to get <= to a value
    # the ccdf (complementary cdf) aka suvival function (scumf) is 1 - cdf
    # return (math.exp(-l)*(l**k))/math.factorial(k)

# test for n or fewer events if expect 1 event, so should be nearly one
def test(n):
    sum=0
    for a in range(0,n+1):  # stops at n events
        sum=sum+p(a,1)
    print(sum)

# cumulative for N or more events
# if you are near the mean, the cum function to the right might double it. If you are far from the mean, you'll get 
# a 10% boost or so
# cum(15,1) gives 3e-13 which is Jay Bonnar super conservative (more realistic is (15, .25)) since 1 death in a 10 year period
# for autism, let's assume kids 1 to 4 get austim so a 3 year window. Your chance of autism is 1/35.
# 3 years is 1,000 days. So in a given day, a child has a 1 in 35,000 chance of getting autism. 
# but a family of 3 would have a 1/10000 chance of having an autistic child on a given day
# so cum(3,.0001)
# if kids get autism only over a 1 year window, use cum(3, 3/(365*35)) because you have 3 kids
# so 2e-12, but there are only 1e8 households in America

# USC is cum(2, .01) which is about 1 in million probability that two once per 100 years happens 

# jay saw 4 people die from the vaccine
# jay saw 14000 shots in his friends. So he should see 14000/1M deaths. He saw 4
# cum(4, .014) which is 1.5e-9
# I think there is a 1 in 1000 kill rate, so jay saw 15, and expected 14.... 

# SIDS >>> cum(225, 10) returns 3.771860150422966e-213
# SIDS is 50% of 100 cases investigated happened within 48 hours of vaccine
# sweet spot of death was 6 months
# want age at death, days after vaccine for every case when asked for 100 cases
# if kids vaccinated every 60 days, chance of this happening is 1/30 so for 90 cases, expect 3, but get 45
# which is 1e-36. If 2x as many cases, it is 1e-71

# saracina lost both brothers to the vax
# she expected 3yr*2 brothers*1e-6 events and saw two
# cum(2, 6e-6)
# 1.8e-11 so 1 in 55 billion people will see that.

# what's the chance I saw a person that had this happen to them? 100x that since I know 100 friends
# cum(1, 1.8e-9) = 1.8 e-9   pretty unlikely


def cum_old(n,m, num_extra=10):
    sum=0
    for a in range(n,n+num_extra+1):  # stops at n events
        prob=p(a,m)
        print(a, prob, sum)
        sum+=prob
    print(sum)

# chance of >=n events given expected m events
# Note that for a given n,m, poisson.cdf + poisson.sf =1
# The cdf includes 0 to n events
# Note that its more likely you'll get 10X fewer events than expected
# than 10X more events than expected due to shape of the curve
# so if a study finds vaxxed and unvaxxed got same amount of deaths
# that is very unlikely
def cum(n,m):
    # answer=poisson.sf(n,m)+poisson.pmf(n,m)   # one way to do it
    return(poisson.sf(n-1,m))                    # the way more clever way to do it

# Jennifer chubb police officer in omaha police dept is 250 cases, 50% happened within 48 hours. But 1/15 should have happened
# within 48 hours. Expected 16.6, but got 125. cum(125,16.6) is 1.2e-64 and 86.4%
# of SIDS deaths were caused by the vaccine

# use shift-enter to run code (control-enter in R)

# cum is good if observed a lot of deaths and expected a few
# but there are also cases where you should have seen 100 execess deaths and got 1 or zero
# that is the pdf. E.g., cdf(1, 100) for chance of seeing 1 or fewer deaths
# when expecting 100.

# chance of seeing n or fewer events when expecting m events
# this is the inverse of cum
def cdf(n,m):
    return(poisson.cdf(n,m))
# note that cdf(1,10) + cum(2,10) =1

# use cum for more than mean 
# use cdf functions for events happening less than the mean
# use pmf for the probability of getting that value exactly.
