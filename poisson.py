'''
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
essentially 0
'''

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
# USC is cum(2, .01) which is about 1 in million probability that two once per 100 years happens 

# jay saw 4 people die from the vaccine
# jay saw 14000 shots in his friends. So he should see 14000/1M deaths. He saw 4
# cum(4, .014) which is 1.5e-9
# I think there is a 1 in 1000 kill rate, so jay saw 15, and expected 14.... 
# SIDS >>> cum(225, 10) returns 3.771860150422966e-213
def cum_old(n,m, num_extra=10):
    sum=0
    for a in range(n,n+num_extra+1):  # stops at n events
        prob=p(a,m)
        print(a, prob, sum)
        sum+=prob
    print(sum)

# chance of >=N events given expected m events
def cum(n,m):
    # answer=poisson.sf(n,m)+poisson.pmf(n,m)   # one way to do it
    answer=poisson.sf(n-1,m)                    # the way more clever way to do it
    print(answer)
    return(answer)