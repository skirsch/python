# from chatgpt
import statsmodels.api as sm
import scipy.stats as stats

def calculate_odds_ratio_ci_z_p(a, b, c, d, alpha=0.05):
    # Create a 2x2 contingency table
    table = [[a, b], [c, d]]
    
    # Calculate odds ratio, confidence intervals, z-score, and p-value
    result = sm.stats.Table2x2(table)
    odds_ratio = result.oddsratio
    
    ci_low, ci_high = result.oddsratio_confint(alpha=alpha)

        # Calculate z-score and p-value
    odds_ratio, p_value = stats.fisher_exact(table)
    # calc z score which is (log odds ratio) / SE
    z_score = result.log_oddsratio/result.log_oddsratio_se
    
    
    return odds_ratio, (ci_low, ci_high), z_score, p_value
    
    
# for vaccine in nursing homes
c = 5864      # dead unvaxxed
d = 677     # dead vaxxed (exposed; bad outcome)
a = 34130-c    # alive unvax = total unvaxxed - dead
b = 1742-d    # alive vaxxed = total vaxxed participants - dead

# use this function if give as good(control), good(experiment), dead(control), dead(experiment)
# where good means a favorable outcome, e.g., healthy, e.g., got 0 covid infections
def odds(a,b,c,d):
    odds_ratio, confidence_interval, z_score, p_value = calculate_odds_ratio_ci_z_p(a, b, c, d)

    print("Odds Ratio:", odds_ratio)
    print("Confidence Interval:", confidence_interval)
    print("Z-Score:", z_score)
    print("P-Value:", p_value)

# use odds2 if have TOTAL count unvaxxed, TOTAL count vaxxed, unvaxxed dead, vaxxed dead

def odds2(a,b,c,d):
    odds(a-c, b-d, c,d)

odds(a,b,c,d)