# Create a file with a column with "-" in between X and Y values
# will do a separate regression for each Y column
# columnns must all be numbers

import pandas as pd
import statsmodels.api as sm

def multiple_regression_with_multiple_y(filename):
    # Read the CSV file
    # data = pd.read_csv(filename)
    data = pd.read_excel(filename, sheet_name="regression")

    
    # columns numbered 0 onwards. index=exact col number with text
    start_col_index=data.columns.get_loc('x') 
    sep_col_index = data.columns.get_loc('y')   # y values start after this 
    end_col_index=data.columns.get_loc('end')  # stop here
    
    # Split data into X and Y based on the blank column
    X = data.iloc[:, start_col_index+1:sep_col_index]  # Columns before the blank column
    Y = data.iloc[:, sep_col_index + 1: end_col_index]  # Columns after the blank column
    
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
    filename= "regression.xlsx"
    filename = "../debate/ACM v3.xlsx"  # xls with regression sheet
    filename = "../debate/California.xlsx"  # xls with regression sheet

    # Run the regression and display the results
    regression_results = multiple_regression_with_multiple_y(filename)
    for y_var, summary in regression_results.items():
        print(f"Regression Results for {y_var}:\n")
        print(summary)
        print("\n" + "="*80 + "\n")
run()
