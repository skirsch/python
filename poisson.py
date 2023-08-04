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
#  
import math
def p(k,l):
    return (math.exp(-l)*(l**k))/math.factorial(k)
