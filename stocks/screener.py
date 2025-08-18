#!/usr/bin/env python3
"""
Analyze stock data from closes_10y.csv
For each stock symbol, compute exponential regression on a specified date range.
Outputs: symbol, slope, R² for exponential fit.
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# CONFIGURATION - Set your analysis period
# ==========================================
ANALYSIS_START_DATE = "2021-08-18"  # Start date for curve fitting (YYYY-MM-DD)
ANALYSIS_END_DATE = "2023-08-18"    # End date for curve fitting (YYYY-MM-DD)
NUM_TICKERS = 50  # Number of tickers to output to stocks/tickers.xlsx file
# ==========================================

def exponential_regression(x, y):
    """
    Perform exponential regression: y = a * exp(b * x)
    Taking log: ln(y) = ln(a) + b * x
    Returns slope (b), R², and whether fit is valid
    """
    try:
        # Remove any zero or negative values for log transformation
        valid_mask = y > 0
        if valid_mask.sum() < 10:  # Need at least 10 points
            return None, None, False
            
        x_valid = x[valid_mask]
        y_valid = y[valid_mask]
        
        # Take natural log of y values
        ln_y = np.log(y_valid)
        
        # Perform linear regression on (x, ln(y))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid, ln_y)
        
        r_squared = r_value ** 2
        
        return slope, r_squared, True
        
    except (ValueError, RuntimeError, np.linalg.LinAlgError):
        return None, None, False

def main():
    print("[INFO] Loading stock data...")
    df = pd.read_csv('stocks/closes_10y.csv')
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Use the configured analysis period
    start_date = datetime.strptime(ANALYSIS_START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(ANALYSIS_END_DATE, "%Y-%m-%d")
    
    print(f"[INFO] Analyzing data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Filter to the specified date range (inclusive)
    analysis_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    
    if analysis_df.empty:
        print("[ERROR] No data found in the specified date range!")
        return
    
    # Get unique tickers in the analysis period
    tickers = analysis_df['ticker'].unique()
    print(f"[INFO] Analyzing {len(tickers)} symbols...")
    
    results = []
    
    for i, ticker in enumerate(tickers):
        if i % 50 == 0:
            print(f"[INFO] Processing {i+1}/{len(tickers)}: {ticker}")
        
        # Get data for this ticker
        ticker_data = analysis_df[analysis_df['ticker'] == ticker].copy()
        
        if len(ticker_data) < 100:  # Need sufficient data points
            continue
            
        # Sort by date
        ticker_data = ticker_data.sort_values('date')
        
        # Create numeric time series (days since start)
        ticker_data['days'] = (ticker_data['date'] - ticker_data['date'].min()).dt.days
        
        x = ticker_data['days'].values
        y = ticker_data['close'].values
        
        # Perform exponential regression
        slope, r_squared, is_valid = exponential_regression(x, y)
        
        if is_valid and slope is not None and r_squared is not None:
            # Convert slope to annualized growth rate
            # slope is per day, multiply by 365 for annual rate
            annual_slope = slope * 365
            
            results.append({
                'ticker': ticker,
                'slope': annual_slope,
                'r_squared': r_squared,
                'data_points': len(ticker_data)
            })
    
    print(f"\n[INFO] Successfully analyzed {len(results)} symbols")
    
    # Convert to DataFrame and sort by R²
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('r_squared', ascending=False)
    
    # Display results
    print("\n" + "="*80)
    print(f"EXPONENTIAL REGRESSION RESULTS ({ANALYSIS_START_DATE} to {ANALYSIS_END_DATE})")
    print("="*80)
    print(f"{'Ticker':<8} {'Annual Slope':<12} {'R²':<8} {'Data Points':<12}")
    print("-" * 80)
    
    for _, row in results_df.head(20).iterrows():
        print(f"{row['ticker']:<8} {row['slope']:<12.4f} {row['r_squared']:<8.4f} {row['data_points']:<12}")
    
    # Save to CSV
    output_file = 'stocks/exponential_regression_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\n[INFO] Full results saved to: {output_file}")
    
    # Summary statistics
    analysis_period = (end_date - start_date).days / 365.25
    print(f"\nSUMMARY STATISTICS:")
    print(f"Analysis Period:        {analysis_period:.2f} years ({ANALYSIS_START_DATE} to {ANALYSIS_END_DATE})")
    print(f"Total symbols analyzed: {len(results_df)}")
    print(f"Average R²: {results_df['r_squared'].mean():.4f}")
    print(f"Median annual slope: {results_df['slope'].median():.4f}")
    print(f"Best fit (highest R²): {results_df.iloc[0]['ticker']} (R² = {results_df.iloc[0]['r_squared']:.4f})")
    
    # Show best and worst performers by slope
    print(f"\nBEST PERFORMERS (highest exponential growth):")
    top_growth = results_df.nlargest(5, 'slope')
    for _, row in top_growth.iterrows():
        print(f"  {row['ticker']}: {row['slope']:.4f} annual slope, R² = {row['r_squared']:.4f}")
        
    print(f"\nWORST PERFORMERS (lowest/most negative exponential growth):")
    bottom_growth = results_df.nsmallest(5, 'slope')
    for _, row in bottom_growth.iterrows():
        print(f"  {row['ticker']}: {row['slope']:.4f} annual slope, R² = {row['r_squared']:.4f}")
    
    # Create tickers.xlsx with top performers by slope
    print(f"\n[INFO] Creating tickers.xlsx with top {NUM_TICKERS} performers by slope...")
    
    # Get top NUM_TICKERS by slope (highest exponential growth)
    top_performers = results_df.nlargest(NUM_TICKERS, 'slope')
    
    # Create DataFrame for Excel output
    tickers_output = pd.DataFrame({
        'ticker': top_performers['ticker'].values,
        'annual_slope': top_performers['slope'].values,
        'r_squared': top_performers['r_squared'].values,
        'data_points': top_performers['data_points'].values
    })
    
    # Save to Excel
    tickers_file = 'stocks/tickers.xlsx'
    tickers_output.to_excel(tickers_file, index=False)
    print(f"[INFO] Top {NUM_TICKERS} ticker symbols saved to: {tickers_file}")
    
    # Show what was saved
    print(f"\nTOP {NUM_TICKERS} TICKERS SAVED TO EXCEL:")
    print(f"{'Rank':<5} {'Ticker':<8} {'Annual Slope':<12} {'R²':<8}")
    print("-" * 35)
    for i, (_, row) in enumerate(top_performers.iterrows(), 1):
        print(f"{i:<5} {row['ticker']:<8} {row['slope']:<12.4f} {row['r_squared']:<8.4f}")

if __name__ == "__main__":
    main()
