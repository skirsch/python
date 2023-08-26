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

def odds(a,b,c,d):
    odds_ratio, confidence_interval, z_score, p_value = calculate_odds_ratio_ci_z_p(a, b, c, d)

    print("Odds Ratio:", odds_ratio)
    print("Confidence Interval:", confidence_interval)
    print("Z-Score:", z_score)
    print("P-Value:", p_value)

odds(a,b,c,d)