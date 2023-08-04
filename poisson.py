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

# chance of getting K events where you expect l chance 
# of getting an event in the period
# so k=15, l=.1 where 1/10 chance of getting one event
# # since tail is very small, if you compute value for say 15 events and expecting 1, 
# cum probab in tail is at most double that value


#  
import math
# chance of getting exactly k events when expect l events
def p(k,l):
    return (math.exp(-l)*(l**k))/math.factorial(k)

# test for n or fewer events if expect 1 event, so should be nearly one
def test(n):
    sum=0
    for a in range(0,n+1):  # stops at n events
        sum=sum+p(a,1)
    print(sum)

# cumulative for N or more events
# if you are near the mean, the cum function to the right might double it. If you are far from the mean, you'll get 
# a 10% boost or so
# cum(15,1) gives 3e-13
def cum(n,m, num_extra=10):
    sum=0
    for a in range(n,n+num_extra+1):  # stops at n events
        prob=p(a,m)
        print(a, prob, sum)
        sum+=prob
    print(sum)