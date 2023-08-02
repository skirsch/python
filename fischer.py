import scipy
# say vaccine is making things worse with more deaths
# ORDER is no treat/ok, treatment/ok,   noT/bad, T/bad,

# this gives a statistic of 10 since odds of damage is 10X greater with the vax
print(scipy.stats.fisher_exact([[10, 100], [1, 100]]))   # two-sided p-value .01  odds ratio is 10X
print(scipy.stats.fisher_exact([[10, 100], [1, 100]], 'greater'))  # one-sided p-value if hypothesis of harm only


