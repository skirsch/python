# portfolio manager for stocks
# This module manages a portfolio of stocks, allowing for analysis and performance tracking.

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Try to import openpyxl for Excel export, install if missing
try:
    import openpyxl
except ImportError:
    print("[INFO] Installing openpyxl for Excel export...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import openpyxl

# ==========================================
# CONFIGURATION - Set your analysis period
# ==========================================
ANALYSIS_START_DATE = "2010-08-18"  # Start date for the portfolio analysis (YYYY-MM-DD)
ANALYSIS_END_DATE = "2025-08-18"    # End date for the analysis (YYYY-MM-DD)

NUM_TICKERS = 10 # Number of tickers to hold in the portfolio
NUM_MONTHS_BACK = 18  # Number of months to look back for analysis
REBALANCE_PERIOD = 6  # Number of months between rebalances

INITIAL_INVESTMENT_PER_STOCK = 1000  # Initial investment per stock ($)
MIN_R_SQUARED = 0 # Minimum R² value for a valid regression, e.g., 0.8 (can make things worse!)

ALGORITHM = "exponential"  # Algorithm to use for screening stocks

MONTHS_BETWEEN_ENTRIES=1  # Months between each instance of the portfolio 
NUM_OF_ENTRIES=6  # Number of times to enter the portfolio

# ALGORITHM = "best return"  # Algorithm to use for screening stocks
# ALGORITHM= "linear"  # Algorithm to use for screening stocks (terrible results)

# ==========================================

def exponential_regression(x, y):
    """
    Perform exponential regression: y = a * exp(b * x)
    Taking log: ln(y) = ln(a) + b * x
    Returns slope (b), R², and whether fit is valid
    """
    try:
        # Remove any zero or negative values for log transformation
        valid_mask = (y > 0) & np.isfinite(y) & np.isfinite(x)
        if valid_mask.sum() < 10:  # Need at least 10 points
            return None, None, False
            
        x_valid = x[valid_mask]
        y_valid = y[valid_mask]
        
        # Take natural log of y values
        ln_y = np.log(y_valid)
        
        # Check for any infinite or NaN values after log
        if not (np.isfinite(ln_y).all() and np.isfinite(x_valid).all()):
            return None, None, False
        
        # Perform linear regression on (x, ln(y))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid, ln_y)
        
        # Check for valid results
        if not (np.isfinite(slope) and np.isfinite(r_value)):
            return None, None, False
        
        r_squared = r_value ** 2
        
        return slope, r_squared, True
        
    except (ValueError, RuntimeError, np.linalg.LinAlgError, OverflowError):
        return None, None, False

def linear_regression(x, y):
    """
    Perform simple linear regression: y = a + b * x
    Returns slope (b), R², and whether fit is valid
    """
    try:
        # Remove any NaN or infinite values
        valid_mask = np.isfinite(y) & np.isfinite(x)
        if valid_mask.sum() < 10:  # Need at least 10 points
            return None, None, False
            
        x_valid = x[valid_mask]
        y_valid = y[valid_mask]
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid, y_valid)
        
        # Check for valid results
        if not (np.isfinite(slope) and np.isfinite(r_value)):
            return None, None, False
        
        r_squared = r_value ** 2
        
        return slope, r_squared, True
        
    except (ValueError, RuntimeError, np.linalg.LinAlgError, OverflowError):
        return None, None, False

def screen_stocks(df, screen_date, num_months_back, num_tickers):
    """
    Screen stocks based on selected algorithm over the past num_months_back months.
    Returns list of top tickers.
    """
    print(f"[INFO] Starting stock screening for {screen_date.strftime('%Y-%m-%d')} using '{ALGORITHM}' algorithm...")
    
    # Calculate lookback start date
    lookback_start = screen_date - timedelta(days=num_months_back * 30.44)  # Average days per month
    
    # Filter data to the screening period
    screen_df = df[(df['date'] >= lookback_start) & (df['date'] <= screen_date)].copy()
    
    if screen_df.empty:
        return []
    
    # Get unique tickers in the screening period
    tickers = screen_df['ticker'].unique()
    print(f"[INFO] Analyzing {len(tickers)} stocks for screening...")
    
    results = []
    
    for i, ticker in enumerate(tickers):
        ticker_data = screen_df[screen_df['ticker'] == ticker].copy()
        
        if len(ticker_data) < 50:  # Need sufficient data points
            continue
            
        # Sort by date and create time series
        ticker_data = ticker_data.sort_values('date')
        
        if ALGORITHM == "best return":
            # Calculate simple percentage return from start to end of period
            start_price = ticker_data['close'].iloc[0]
            end_price = ticker_data['close'].iloc[-1]
            
            if start_price > 0:  # Avoid division by zero
                pct_return = (end_price - start_price) / start_price * 100
                
                results.append({
                    'ticker': ticker,
                    'return': pct_return,
                    'start_price': start_price,
                    'end_price': end_price,
                    'data_points': len(ticker_data)
                })
        
        elif ALGORITHM == "exponential":
            # Use exponential regression (original method)
            ticker_data['days'] = (ticker_data['date'] - ticker_data['date'].min()).dt.days
            
            x = ticker_data['days'].values
            y = ticker_data['close'].values
            
            # Perform exponential regression
            slope, r_squared, is_valid = exponential_regression(x, y)
            
            if is_valid and slope is not None and r_squared is not None and r_squared >= MIN_R_SQUARED:
                # Convert slope to annualized growth rate
                annual_slope = slope * 365
                
                results.append({
                    'ticker': ticker,
                    'slope': annual_slope,
                    'r_squared': r_squared,
                    'data_points': len(ticker_data)
                })
        
        elif ALGORITHM == "linear":
            # Use linear regression
            ticker_data['days'] = (ticker_data['date'] - ticker_data['date'].min()).dt.days
            
            x = ticker_data['days'].values
            y = ticker_data['close'].values
            
            # Perform linear regression
            slope, r_squared, is_valid = linear_regression(x, y)
            
            if is_valid and slope is not None and r_squared is not None and r_squared >= MIN_R_SQUARED:
                # Convert slope to annualized growth rate (slope is price change per day)
                annual_slope = slope * 365
                
                results.append({
                    'ticker': ticker,
                    'slope': annual_slope,
                    'r_squared': r_squared,
                    'data_points': len(ticker_data)
                })
    
    # Sort results based on algorithm
    results_df = pd.DataFrame(results)
    if results_df.empty:
        if ALGORITHM in ["exponential", "linear"]:
            print(f"[WARN] No valid results from screening! (R² >= {MIN_R_SQUARED:.2f} required)")
        else:
            print(f"[WARN] No valid results from screening!")
        return []
    
    if ALGORITHM == "best return":
        top_stocks = results_df.nlargest(num_tickers, 'return')
        print(f"[INFO] Screening complete. Selected {len(top_stocks)} stocks from {len(results)} candidates based on highest returns.")
    else:  # exponential or linear
        top_stocks = results_df.nlargest(num_tickers, 'slope')
        print(f"[INFO] Screening complete. Selected {len(top_stocks)} stocks from {len(results)} valid candidates (R² >= {MIN_R_SQUARED:.2f}).")
    
    return top_stocks['ticker'].tolist()

def get_rebalance_dates(start_date, end_date, rebalance_period_months):
    """
    Generate list of rebalance dates from start to end, spaced by rebalance_period_months.
    """
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        dates.append(current_date)
        # Add months (approximate)
        next_month = current_date.month + rebalance_period_months
        next_year = current_date.year
        
        while next_month > 12:
            next_month -= 12
            next_year += 1
            
        try:
            current_date = current_date.replace(year=next_year, month=next_month)
        except ValueError:  # Handle end of month edge cases
            if next_month == 2 and current_date.day > 28:
                current_date = current_date.replace(year=next_year, month=next_month, day=28)
            else:
                current_date = current_date.replace(year=next_year, month=next_month, day=1)
                current_date = current_date + timedelta(days=30)
    
    return dates

def calculate_single_portfolio_performance(df, start_date, end_date, num_tickers, num_months_back, 
                                         rebalance_period, initial_investment_per_stock, price_lookup, portfolio_id=0):
    """
    Calculate performance for a single portfolio instance.
    """
    # Get rebalance dates
    rebalance_dates = get_rebalance_dates(start_date, end_date, rebalance_period)
    
    # Initialize portfolio tracking
    portfolio_history = []
    current_holdings = {}  # {ticker: shares}
    cash = 0
    trades_log = []  # Track all buy/sell transactions
    
    print(f"[INFO] Portfolio {portfolio_id+1} simulation from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Get all trading dates in the analysis period
    analysis_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    all_dates = sorted(analysis_df['date'].unique())
    
    current_portfolio_tickers = []
    last_rebalance_date = None
    
    for i, date in enumerate(all_dates):
        # Check if this is a rebalance date - only rebalance at specific intervals
        should_rebalance = False
        
        if not current_holdings:
            # First rebalance
            should_rebalance = True
        else:
            # Check if enough time has passed since last rebalance
            for rebalance_date in rebalance_dates:
                if abs((date - rebalance_date).days) <= 3:  # Within 3 days of scheduled rebalance
                    if last_rebalance_date is None or (date - last_rebalance_date).days >= (rebalance_period * 30 - 10):
                        should_rebalance = True
                        break
        
        if should_rebalance:
            print(f"[INFO] Portfolio {portfolio_id+1} rebalancing on {date.strftime('%Y-%m-%d')}")
            last_rebalance_date = date
            
            # Screen for new portfolio
            new_tickers = screen_stocks(df, date, num_months_back, num_tickers)
            
            if not new_tickers:
                print(f"[WARN] Portfolio {portfolio_id+1}: No stocks screened on {date.strftime('%Y-%m-%d')}, keeping current portfolio")
            else:
                # Calculate current portfolio value
                current_value = cash
                for ticker, shares in current_holdings.items():
                    current_price = price_lookup.get((ticker, date))
                    if current_price is not None:
                        current_value += shares * current_price
                
                # Sell all current holdings
                for ticker, shares in current_holdings.items():
                    current_price = price_lookup.get((ticker, date))
                    if current_price is not None:
                        sell_amount = shares * current_price
                        cash += sell_amount
                        
                        # Log the sell transaction
                        trades_log.append({
                            'portfolio_id': portfolio_id + 1,
                            'date': date,
                            'ticker': ticker,
                            'action': 'SELL',
                            'quantity': shares,
                            'price': current_price,
                            'dollar_amount': sell_amount
                        })
                
                current_holdings = {}
                
                # If this is the first rebalance, use initial investment
                if current_value == 0:
                    total_investment = len(new_tickers) * initial_investment_per_stock
                    cash = total_investment
                    current_value = total_investment
                
                # Buy new holdings (equal dollar amounts)
                dollars_per_stock = cash / len(new_tickers)
                
                for ticker in new_tickers:
                    current_price = price_lookup.get((ticker, date))
                    if current_price is not None:
                        shares = dollars_per_stock / current_price
                        current_holdings[ticker] = shares
                        buy_amount = shares * current_price
                        cash -= buy_amount
                        
                        # Log the buy transaction
                        trades_log.append({
                            'portfolio_id': portfolio_id + 1,
                            'date': date,
                            'ticker': ticker,
                            'action': 'BUY',
                            'quantity': shares,
                            'price': current_price,
                            'dollar_amount': buy_amount
                        })
                
                current_portfolio_tickers = new_tickers
                print(f"[INFO] Portfolio {portfolio_id+1}: {len(new_tickers)} stocks, value: ${current_value:,.2f}")
        
        # Calculate daily portfolio value
        portfolio_value = cash
        
        for ticker, shares in current_holdings.items():
            current_price = price_lookup.get((ticker, date))
            if current_price is not None:
                portfolio_value += shares * current_price
            else:
                # Use last known price if current price is unavailable
                # Look back up to 30 days for the most recent price
                price_found = None
                days_back = 0
                for lookback_days in range(1, 31):
                    lookback_date = date - timedelta(days=lookback_days)
                    price_found = price_lookup.get((ticker, lookback_date))
                    if price_found is not None:
                        days_back = lookback_days
                        break
                
                if price_found is not None:
                    portfolio_value += shares * price_found
                else:
                    # If no price found in last 30 days, assume stock is worthless
                    pass  # Don't add to portfolio value
        
        portfolio_history.append({
            'date': date,
            'portfolio_value': portfolio_value,
            'num_holdings': len(current_holdings),
            'cash': cash,
            'portfolio_id': portfolio_id
        })
    
    return pd.DataFrame(portfolio_history), trades_log

def calculate_portfolio_performance(df, start_date, end_date, num_tickers, num_months_back, 
                                  rebalance_period, initial_investment_per_stock):
    """
    Calculate portfolio performance with multiple parallel portfolios for smoother returns.
    """
    print(f"[INFO] Running {NUM_OF_ENTRIES} parallel portfolios with {MONTHS_BETWEEN_ENTRIES} month offsets")
    
    # Get all trading dates in the analysis period
    analysis_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    all_dates = sorted(analysis_df['date'].unique())
    
    # PRE-INDEX DATA FOR FAST LOOKUPS
    print(f"[INFO] Pre-indexing price data for fast lookups...")
    price_lookup = {}
    for _, row in analysis_df.iterrows():
        key = (row['ticker'], row['date'])
        price_lookup[key] = row['close']
    print(f"[INFO] Indexed {len(price_lookup)} price data points")
    
    # Create start dates for each portfolio (offset by MONTHS_BETWEEN_ENTRIES)
    portfolio_start_dates = []
    for i in range(NUM_OF_ENTRIES):
        offset_months = i * MONTHS_BETWEEN_ENTRIES
        portfolio_start = start_date
        
        # Add months to start date
        new_month = portfolio_start.month + offset_months
        new_year = portfolio_start.year
        
        while new_month > 12:
            new_month -= 12
            new_year += 1
            
        try:
            portfolio_start = portfolio_start.replace(year=new_year, month=new_month)
        except ValueError:  # Handle end of month edge cases
            portfolio_start = portfolio_start.replace(year=new_year, month=new_month, day=1)
        
        portfolio_start_dates.append(portfolio_start)
    
    print(f"[INFO] Portfolio start dates:")
    for i, start_dt in enumerate(portfolio_start_dates):
        print(f"  Portfolio {i+1}: {start_dt.strftime('%Y-%m-%d')}")
    
    # Run each portfolio and collect results
    all_portfolio_results = []
    all_trades = []  # Collect all trades from all portfolios
    
    for i in range(NUM_OF_ENTRIES):
        portfolio_start = portfolio_start_dates[i]
        if portfolio_start <= end_date:  # Only run if start date is before end date
            print(f"\n[INFO] Starting Portfolio {i+1} from {portfolio_start.strftime('%Y-%m-%d')}")
            portfolio_df, trades_log = calculate_single_portfolio_performance(
                df, portfolio_start, end_date, num_tickers, num_months_back,
                rebalance_period, initial_investment_per_stock, price_lookup, i
            )
            if not portfolio_df.empty:
                all_portfolio_results.append(portfolio_df)
                all_trades.extend(trades_log)  # Add trades from this portfolio
    
    if not all_portfolio_results:
        print("[ERROR] No portfolio data generated!")
        return pd.DataFrame(), []
    
    # Combine all portfolio results into a single aggregated portfolio
    print(f"\n[INFO] Combining results from {len(all_portfolio_results)} portfolios...")
    
    # Get all unique dates across all portfolios
    all_unique_dates = set()
    for portfolio_df in all_portfolio_results:
        all_unique_dates.update(portfolio_df['date'])
    all_unique_dates = sorted(list(all_unique_dates))
    
    # Create combined portfolio history
    combined_history = []
    
    for date in all_unique_dates:
        total_value = 0
        total_holdings = 0
        total_cash = 0
        active_portfolios = 0
        
        # Sum values from all active portfolios on this date
        for portfolio_df in all_portfolio_results:
            portfolio_data = portfolio_df[portfolio_df['date'] == date]
            if not portfolio_data.empty:
                row = portfolio_data.iloc[0]
                total_value += row['portfolio_value']
                total_holdings += row['num_holdings']
                total_cash += row['cash']
                active_portfolios += 1
        
        if active_portfolios > 0:
            combined_history.append({
                'date': date,
                'portfolio_value': total_value,
                'num_holdings': total_holdings,
                'cash': total_cash,
                'active_portfolios': active_portfolios
            })
    
    combined_df = pd.DataFrame(combined_history)
    print(f"[INFO] Combined portfolio spans {len(combined_df)} trading days with up to {NUM_OF_ENTRIES} active portfolios")
    
    return combined_df, all_trades

def analyze_performance(portfolio_df):
    """
    Analyze portfolio performance and generate statistics.
    """
    if portfolio_df.empty:
        return
    
    # Calculate the actual total initial investment (accounts for parallel portfolios)
    actual_initial_investment = NUM_OF_ENTRIES * NUM_TICKERS * INITIAL_INVESTMENT_PER_STOCK
    
    # Calculate returns
    portfolio_df['daily_return'] = portfolio_df['portfolio_value'].pct_change().fillna(0)
    
    # Adjust initial value for proper return calculation
    first_portfolio_value = portfolio_df['portfolio_value'].iloc[0]
    portfolio_df['cumulative_return'] = (portfolio_df['portfolio_value'] / actual_initial_investment - 1) * 100
    
    # Calculate drawdown
    rolling_max = portfolio_df['portfolio_value'].expanding().max()
    portfolio_df['drawdown'] = (portfolio_df['portfolio_value'] - rolling_max) / rolling_max * 100
    
    # Monthly returns
    portfolio_df['month_year'] = portfolio_df['date'].dt.to_period('M')
    monthly_returns = portfolio_df.groupby('month_year')['daily_return'].apply(lambda x: (1 + x).prod() - 1) * 100
    
    # Annual returns
    portfolio_df['year'] = portfolio_df['date'].dt.year
    annual_returns = portfolio_df.groupby('year')['daily_return'].apply(lambda x: (1 + x).prod() - 1) * 100
    
    # Performance statistics - use actual initial investment
    initial_value = actual_initial_investment  # Corrected initial value
    final_value = portfolio_df['portfolio_value'].iloc[-1]
    total_return = (final_value / initial_value - 1) * 100
    
    days_total = len(portfolio_df)
    years = days_total / 252
    annualized_return = (final_value / initial_value) ** (1/years) - 1 if years > 0 else 0
    
    daily_vol = portfolio_df['daily_return'].std()
    annualized_vol = daily_vol * np.sqrt(252)
    
    sharpe_ratio = annualized_return / annualized_vol if annualized_vol > 0 else 0
    max_drawdown = portfolio_df['drawdown'].min()
    
    # Print configuration parameters
    print(f"\n{'='*60}")
    print("CONFIGURATION PARAMETERS")
    print(f"{'='*60}")
    print(f"Analysis Period:         {ANALYSIS_START_DATE} to {ANALYSIS_END_DATE}")
    print(f"Portfolio Size:          {NUM_TICKERS} stocks per portfolio")
    print(f"Screening Lookback:      {NUM_MONTHS_BACK} months")
    print(f"Rebalancing Period:      {REBALANCE_PERIOD} months")
    print(f"Initial Investment:      ${INITIAL_INVESTMENT_PER_STOCK:,.0f} per stock")
    print(f"Minimum R²:              {MIN_R_SQUARED:.2f}")
    print(f"Algorithm:               {ALGORITHM}")
    print(f"Parallel Portfolios:     {NUM_OF_ENTRIES}")
    print(f"Entry Offset:            {MONTHS_BETWEEN_ENTRIES} month(s)")
    print(f"Total Investment:        ${actual_initial_investment:,.0f}")
    
    # Print performance summary
    print(f"\n{'='*60}")
    print("PORTFOLIO PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"Initial Portfolio Value: ${initial_value:,.2f}")
    print(f"Final Portfolio Value:   ${final_value:,.2f}")
    print(f"Total Return:            {total_return:.2f}%")
    print(f"Annualized Return:       {annualized_return*100:.2f}%")
    print(f"Annualized Volatility:   {annualized_vol*100:.2f}%")
    print(f"Sharpe Ratio:            {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown:        {max_drawdown:.2f}%")
    print(f"Number of Trading Days:  {days_total}")
    
    # Monthly return statistics
    print(f"\nMONTHLY RETURNS STATISTICS:")
    print(f"Best Month:              {monthly_returns.max():.2f}%")
    print(f"Worst Month:             {monthly_returns.min():.2f}%")
    print(f"Average Monthly Return:  {monthly_returns.mean():.2f}%")
    print(f"Monthly Volatility:      {monthly_returns.std():.2f}%")
    
    # Annual returns
    print(f"\nANNUAL RETURNS:")
    for year, ret in annual_returns.items():
        print(f"Year {year}: {ret:.2f}%")
    
    return portfolio_df, monthly_returns, annual_returns

def create_visualizations(portfolio_df, monthly_returns):
    """
    Create performance visualization charts.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Portfolio Performance Analysis', fontsize=16, fontweight='bold')
    
    # Portfolio value over time
    ax1.plot(portfolio_df['date'], portfolio_df['portfolio_value'], 'b-', linewidth=1.5)
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Cumulative returns
    ax2.plot(portfolio_df['date'], portfolio_df['cumulative_return'], 'g-', linewidth=1.5)
    ax2.set_title('Cumulative Returns')
    ax2.set_ylabel('Cumulative Return (%)')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Monthly returns
    ax3.bar(range(len(monthly_returns)), monthly_returns.values, alpha=0.7)
    ax3.set_title('Monthly Returns')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Monthly Return (%)')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    
    # Drawdown
    ax4.fill_between(portfolio_df['date'], portfolio_df['drawdown'], 0, alpha=0.5, color='red')
    ax4.plot(portfolio_df['date'], portfolio_df['drawdown'], 'r-', linewidth=1)
    ax4.set_title('Drawdown')
    ax4.set_ylabel('Drawdown (%)')
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Format x-axis
    for ax in [ax1, ax2, ax4]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save chart
    chart_file = 'stocks/portfolio_performance.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"\n[INFO] Performance chart saved to: {chart_file}")
    
    plt.show()

def main():
    """
    Main portfolio management function.
    """
    # Load data
    print("[INFO] Loading stock data...")
    df = pd.read_csv('stocks/closes_17y.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # Convert configuration dates
    start_date = datetime.strptime(ANALYSIS_START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(ANALYSIS_END_DATE, "%Y-%m-%d")
    
    print(f"[INFO] Portfolio analysis period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"[INFO] Portfolio size: {NUM_TICKERS} stocks")
    print(f"[INFO] Screening lookback: {NUM_MONTHS_BACK} months")
    print(f"[INFO] Rebalancing every: {REBALANCE_PERIOD} months")
    print(f"[INFO] Initial investment: ${INITIAL_INVESTMENT_PER_STOCK:,.0f} per stock")
    
    # Calculate portfolio performance
    portfolio_df, all_trades = calculate_portfolio_performance(
        df, start_date, end_date, NUM_TICKERS, NUM_MONTHS_BACK, 
        REBALANCE_PERIOD, INITIAL_INVESTMENT_PER_STOCK
    )
    
    if portfolio_df.empty:
        print("[ERROR] No portfolio data generated!")
        return
    
    # Analyze performance
    portfolio_df, monthly_returns, annual_returns = analyze_performance(portfolio_df)
    
    # Save results
    output_file = 'stocks/portfolio_results.csv'
    portfolio_df.to_csv(output_file, index=False)
    print(f"\n[INFO] Portfolio results saved to: {output_file}")
    
    # Save trades to Excel file
    if all_trades:
        trades_df = pd.DataFrame(all_trades)
        trades_df = trades_df.sort_values(['date', 'portfolio_id', 'ticker'])
        
        # Format the trades DataFrame for better readability
        trades_df['date'] = trades_df['date'].dt.strftime('%Y-%m-%d')
        trades_df['quantity'] = trades_df['quantity'].round(4)
        trades_df['price'] = trades_df['price'].round(2)
        trades_df['dollar_amount'] = trades_df['dollar_amount'].round(2)
        
        # Rename columns for Excel
        trades_df = trades_df.rename(columns={
            'portfolio_id': 'Portfolio',
            'date': 'Date',
            'ticker': 'Ticker',
            'action': 'Action',
            'quantity': 'Quantity',
            'price': 'Price',
            'dollar_amount': 'Dollar_Amount'
        })
        
        trades_file = 'stocks/trades.xlsx'
        trades_df.to_excel(trades_file, index=False, sheet_name='All_Trades')
        print(f"[INFO] Trades log saved to: {trades_file}")
        print(f"[INFO] Total transactions recorded: {len(trades_df)}")
        
        # Print some trade statistics
        buy_trades = trades_df[trades_df['Action'] == 'BUY']
        sell_trades = trades_df[trades_df['Action'] == 'SELL']
        
        print(f"[INFO] Buy transactions: {len(buy_trades)}")
        print(f"[INFO] Sell transactions: {len(sell_trades)}")
        print(f"[INFO] Total buy amount: ${buy_trades['Dollar_Amount'].sum():,.2f}")
        print(f"[INFO] Total sell amount: ${sell_trades['Dollar_Amount'].sum():,.2f}")
    
    # Create visualizations
    create_visualizations(portfolio_df, monthly_returns)
    
    print(f"\n[DONE] Portfolio analysis complete!")

if __name__ == "__main__":
    main()
