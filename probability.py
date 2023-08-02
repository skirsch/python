from scipy.special import comb

def probability_at_least_k_red_no_green(k, n, N_red, N_green, N_blue):
    probability = 0
    for i in range(k, n + 1):
        probability += (comb(n, i) * comb(N_red, i) * comb(N_green, n - i) * comb(N_blue, n - i)) / comb(N_red + N_green + N_blue, n)
    return probability

# Given information
N_red_balls = 31
N_green_balls = 1875
N_blue_balls = 5595
total_draws = 15

# Calculate probability of at least 3 red balls and no green balls
probability_at_least_3_red_no_green = probability_at_least_k_red_no_green(3, total_draws, N_red_balls, N_green_balls, N_blue_balls)

print(f"The probability of drawing at least 3 red balls and none are green out of 15 draws is: {probability_at_least_3_red_no_green:.3e}")
