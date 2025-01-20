# Create a file with a column with "-" in between X and Y values
# will do a separate regression for each Y column
# columnns must all be numbers

import pandas as pd
import statsmodels.api as sm

def multiple_regression_with_multiple_y(filename, blank_column_name):
    # Read the CSV file
    data = pd.read_csv(filename)
    
    # Find the blank column
    blank_col_index = data.columns.get_loc(blank_column_name)
    
    # Split data into X and Y based on the blank column
    X = data.iloc[:, :blank_col_index]  # Columns before the blank column
    Y = data.iloc[:, blank_col_index + 1:]  # Columns after the blank column
    
    # Perform regression for each Y column
    results = {}
    for y_col in Y.columns:
        y = Y[y_col]
        X_with_const = sm.add_constant(X)  # Add constant for intercept
        model = sm.OLS(y, X_with_const).fit()
        results[y_col] = model.summary()  # Store the summary for each Y column
    
    return results

# Example usage
def run(): 
    filename = "regression.csv"  # Replace with your CSV filename
    blank_column_name = "STOP"  # Replace with the name of the blank column in your dataset

    # Run the regression and display the results
    regression_results = multiple_regression_with_multiple_y(filename, blank_column_name)
    for y_var, summary in regression_results.items():
        print(f"Regression Results for {y_var}:\n")
        print(summary)
        print("\n" + "="*80 + "\n")
run()
