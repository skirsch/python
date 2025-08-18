#!/usr/bin/env python3
"""
Generate daily equity curve for a portfolio of stocks.
Reads ticker symbols from ticker.xlsx and price data from closes_10y.csv.
Creates an equally dollar-weighted portfolio starting with $1000 per stock.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def main():
    # Read ticker list from Excel file
    print("[INFO] Loading ticker symbols from tickers.xlsx...")
    try:
        tickers_df = pd.read_excel('stocks/tickers.xlsx')
        
        # Try to find the ticker column (could be named various things)
        ticker_col = None
        for col in tickers_df.columns:
            if 'ticker' in col.lower() or 'symbol' in col.lower():
                ticker_col = col
                break
        
        if ticker_col is None:
            # If no obvious column name, use the first column
            ticker_col = tickers_df.columns[0]
            
        tickers = tickers_df[ticker_col].astype(str).str.upper().str.strip().tolist()
        # Remove any NaN values
        tickers = [t for t in tickers if t != 'NAN' and pd.notna(t)]
        
        print(f"[INFO] Found {len(tickers)} ticker symbols: {tickers[:10]}{'...' if len(tickers) > 10 else ''}")
        
    except FileNotFoundError:
        print("[ERROR] ticker.xlsx file not found!")
        return
    except Exception as e:
        print(f"[ERROR] Error reading ticker.xlsx: {e}")
        return
    
    # Read price data
    print("[INFO] Loading price data from closes_10y.csv...")
    try:
        prices_df = pd.read_csv('stocks/closes_10y.csv')
        prices_df['date'] = pd.to_datetime(prices_df['date'])
        
        # Filter to only the tickers we want
        portfolio_data = prices_df[prices_df['ticker'].isin(tickers)].copy()
        
        if portfolio_data.empty:
            print("[ERROR] No matching ticker data found!")
            return
            
        available_tickers = portfolio_data['ticker'].unique()
        missing_tickers = set(tickers) - set(available_tickers)
        
        if missing_tickers:
            print(f"[WARN] Missing data for {len(missing_tickers)} tickers: {list(missing_tickers)[:5]}{'...' if len(missing_tickers) > 5 else ''}")
        
        print(f"[INFO] Using {len(available_tickers)} tickers with available data")
        
    except FileNotFoundError:
        print("[ERROR] closes_10y.csv file not found in stocks/ directory!")
        return
    except Exception as e:
        print(f"[ERROR] Error reading price data: {e}")
        return
    
    # Pivot data to have dates as rows and tickers as columns
    print("[INFO] Processing price data...")
    price_matrix = portfolio_data.pivot(index='date', columns='ticker', values='close')
    
    print(f"[INFO] Price matrix shape before cleaning: {price_matrix.shape} (dates x tickers)")
    print(f"[INFO] Full date range available: {price_matrix.index.min().strftime('%Y-%m-%d')} to {price_matrix.index.max().strftime('%Y-%m-%d')}")
    
    # Filter to last 5 years for analysis BEFORE dropping NaN values
    end_date = price_matrix.index.max()
    start_date_5yr = end_date - pd.Timedelta(days=5*365 + 30)  # Add buffer for weekends/holidays
    
    # Filter to 5-year period first
    price_matrix_5yr = price_matrix.loc[price_matrix.index >= start_date_5yr].copy()
    
    print(f"[INFO] After 5-year filter: {price_matrix_5yr.shape} (dates x tickers)")
    print(f"[INFO] 5-year date range: {price_matrix_5yr.index.min().strftime('%Y-%m-%d')} to {price_matrix_5yr.index.max().strftime('%Y-%m-%d')}")
    
    # Check data availability for each ticker in the 5-year period
    data_coverage = price_matrix_5yr.count() / len(price_matrix_5yr)  # % of non-NaN values
    good_tickers = data_coverage[data_coverage >= 0.95].index.tolist()  # Keep tickers with 95%+ data
    
    print(f"[INFO] Tickers with good 5-year coverage (>=95%): {len(good_tickers)} out of {len(data_coverage)}")
    if len(good_tickers) < len(data_coverage):
        poor_coverage = data_coverage[data_coverage < 0.95].sort_values()
        print(f"[INFO] Removed tickers with poor coverage: {poor_coverage.head().to_dict()}")
    
    # Filter to only good tickers
    price_matrix_5yr = price_matrix_5yr[good_tickers].copy()
    
    # Forward fill missing values (in case of gaps)
    price_matrix_5yr = price_matrix_5yr.fillna(method='ffill')
    
    # Drop any remaining NaN rows (should be minimal now)
    price_matrix_5yr = price_matrix_5yr.dropna()
    
    if price_matrix_5yr.empty:
        print("[ERROR] No valid price data after processing!")
        return
    
    available_start = price_matrix_5yr.index.min()
    actual_end_date = price_matrix_5yr.index.max()
    
    print(f"[INFO] Final analysis period: {available_start.strftime('%Y-%m-%d')} to {actual_end_date.strftime('%Y-%m-%d')}")
    print(f"[INFO] Portfolio starts investing on: {available_start.strftime('%Y-%m-%d')} (first date with complete data for all selected stocks)")
    print(f"[INFO] Final portfolio includes {len(good_tickers)} stocks with complete 5-year data")
    
    # Calculate initial shares for each stock (equal dollar weighting)
    initial_investment = 1000  # $1000 per stock
    first_prices = price_matrix_5yr.iloc[0]  # First day prices in our 5-year window
    
    # Calculate shares: $1000 / price per share
    shares = initial_investment / first_prices
    
    print(f"\n[INFO] Initial portfolio allocation (first {min(5, len(shares))} stocks):")
    for ticker in shares.head().index:
        price = first_prices[ticker]
        num_shares = shares[ticker]
        print(f"  {ticker}: {num_shares:.4f} shares @ ${price:.2f} = ${initial_investment:.2f}")
    
    # Calculate daily portfolio values using 5-year data
    daily_values = price_matrix_5yr.multiply(shares, axis=1)  # shares * prices for each day
    portfolio_value = daily_values.sum(axis=1)  # Sum across all stocks
    
    # Calculate daily returns
    portfolio_returns = portfolio_value.pct_change().fillna(0)
    
    # Calculate cumulative return
    cumulative_return = (portfolio_value / portfolio_value.iloc[0] - 1) * 100
    
    # Calculate some statistics
    initial_value = portfolio_value.iloc[0]
    final_value = portfolio_value.iloc[-1]
    total_return = (final_value / initial_value - 1) * 100
    
    # Annualized return (assuming 252 trading days per year)
    days_total = len(portfolio_value)
    years = days_total / 252
    annualized_return = (final_value / initial_value) ** (1/years) - 1
    
    # Volatility (annualized)
    daily_vol = portfolio_returns.std()
    annualized_vol = daily_vol * np.sqrt(252)
    
    # Sharpe ratio (assuming 0% risk-free rate)
    sharpe_ratio = annualized_return / annualized_vol if annualized_vol > 0 else 0
    
    # Max drawdown
    rolling_max = portfolio_value.expanding().max()
    drawdown = (portfolio_value - rolling_max) / rolling_max * 100
    max_drawdown = drawdown.min()
    
    print(f"\n{'='*60}")
    print("5-YEAR PORTFOLIO PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"Investment Start Date:   {available_start.strftime('%Y-%m-%d')}")
    print(f"Investment End Date:     {actual_end_date.strftime('%Y-%m-%d')}")
    print(f"Investment Period:       {years:.2f} years ({days_total} trading days)")
    print(f"Initial Portfolio Value: ${initial_value:,.2f}")
    print(f"Final Portfolio Value:   ${final_value:,.2f}")
    print(f"Total Return:            {total_return:.2f}%")
    print(f"Average Annual Return:   {annualized_return*100:.2f}%")
    print(f"Annualized Volatility:   {annualized_vol*100:.2f}%")
    print(f"Sharpe Ratio:            {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown:        {max_drawdown:.2f}%")
    
    # Additional 5-year analysis
    print(f"\n5-YEAR PERFORMANCE BREAKDOWN:")
    print(f"Total Portfolio Growth:  ${final_value - initial_value:,.2f}")
    print(f"Growth Multiple:         {final_value / initial_value:.2f}x")
    
    # Year-by-year performance if we have enough data
    if years >= 1:
        yearly_returns = []
        for year_start in range(int(years)):
            year_begin_idx = year_start * 252
            year_end_idx = min((year_start + 1) * 252, len(portfolio_value) - 1)
            
            if year_end_idx < len(portfolio_value):
                year_begin_val = portfolio_value.iloc[year_begin_idx]
                year_end_val = portfolio_value.iloc[year_end_idx]
                year_return = (year_end_val / year_begin_val - 1) * 100
                yearly_returns.append(year_return)
                
                year_begin_date = portfolio_value.index[year_begin_idx]
                year_end_date = portfolio_value.index[year_end_idx]
                print(f"Year {year_start + 1} ({year_begin_date.strftime('%Y-%m-%d')} to {year_end_date.strftime('%Y-%m-%d')}): {year_return:.2f}%")
        
        if yearly_returns:
            avg_yearly_return = np.mean(yearly_returns)
            print(f"\nAverage Yearly Return:   {avg_yearly_return:.2f}%")
            print(f"Best Year:              {max(yearly_returns):.2f}%")
            print(f"Worst Year:             {min(yearly_returns):.2f}%")
    
    # Save results
    results_df = pd.DataFrame({
        'date': portfolio_value.index,
        'portfolio_value': portfolio_value.values,
        'daily_return': portfolio_returns.values,
        'cumulative_return': cumulative_return.values,
        'drawdown': drawdown.values
    })
    
    output_file = 'stocks/equity_curve.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\n[INFO] Equity curve data saved to: {output_file}")
    
    # Create visualization
    print("[INFO] Creating equity curve chart...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Portfolio Performance Analysis', fontsize=16, fontweight='bold')
    
    # Portfolio value over time
    ax1.plot(portfolio_value.index, portfolio_value.values, 'b-', linewidth=1.5)
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Cumulative returns
    ax2.plot(cumulative_return.index, cumulative_return.values, 'g-', linewidth=1.5)
    ax2.set_title('Cumulative Returns')
    ax2.set_ylabel('Cumulative Return (%)')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Daily returns histogram
    ax3.hist(portfolio_returns.values, bins=50, alpha=0.7, edgecolor='black')
    ax3.set_title('Daily Returns Distribution')
    ax3.set_xlabel('Daily Return')
    ax3.set_ylabel('Frequency')
    ax3.axvline(x=0, color='r', linestyle='--', alpha=0.7)
    ax3.grid(True, alpha=0.3)
    
    # Drawdown
    ax4.fill_between(drawdown.index, drawdown.values, 0, alpha=0.5, color='red')
    ax4.plot(drawdown.index, drawdown.values, 'r-', linewidth=1)
    ax4.set_title('Drawdown')
    ax4.set_ylabel('Drawdown (%)')
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Format x-axis for all subplots
    for ax in [ax1, ax2, ax3, ax4]:
        if ax in [ax1, ax2, ax4]:  # Time series plots
            ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save chart
    chart_file = 'stocks/equity_curve_chart.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"[INFO] Chart saved to: {chart_file}")
    
    plt.show()
    
    print(f"\n[DONE] Portfolio analysis complete!")

if __name__ == "__main__":
    main()
