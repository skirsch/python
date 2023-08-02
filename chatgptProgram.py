from scipy.special import comb

'''
I have a jar with red and blue balls. 
There are 31 red balls and 7500 blue balls. 
I randomly take out 15 balls from the jar. 
What is the probability that at least 3 of the balls are red?
'''
def probability_at_least_k_red(k, n, N_red, N_blue):
    probability = 0
    for i in range(k, n + 1):
        probability += (comb(n, i) * comb(N_red, i) * comb(N_blue, n - i)) / comb(N_red + N_blue, n)
    return probability

# Given information
N_red_balls = 31
N_blue_balls = 7500
total_draws = 15

# Calculate probability of at least 3 red balls
probability_at_least_3_red = probability_at_least_k_red(3, total_draws, N_red_balls, N_blue_balls)

print(f"The probability of drawing at least 3 red balls out of 15 draws is: {probability_at_least_3_red:.6f}")
