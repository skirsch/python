#!/usr/bin/env python3
# python extract.py --stooq-zip stocks/data.zip --years 17 --output stocks/closes_17y.csv

"""
Extracts daily closing prices for S&P 500 and QQQ constituents from a Stooq ZIP
file containing historical daily data.
The script fetches the current constituents from Wikipedia and Invesco, maps them
to Stooq symbols, and extracts the last N years of daily closes.


Options you might like

--include sp500,qqq (default) — choose either or both universes

--tickers-csv mytickers.csv — add more tickers (CSV with a Ticker/Symbol column or one column)

--asof 2025-08-18 — set the end date explicitly

--years 10 — change lookback window
"""

import argparse
import csv
import io
import os
import re
import sys
import zipfile
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests

# ------------------------------
# Helpers for constituents
# ------------------------------

def fetch_sp500_symbols() -> pd.Series:
    """
    Fetch current S&P 500 constituents from Wikipedia.
    Returns a pandas Series of ticker symbols (strings).
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        tables = pd.read_html(url)
        for tbl in tables:
            if "Symbol" in tbl.columns:
                syms = tbl["Symbol"].astype(str).str.strip().str.upper()
                return syms.dropna().drop_duplicates()
        raise RuntimeError("Could not find 'Symbol' column on Wikipedia page.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch S&P 500 symbols: {e}")

def try_download(url: str, timeout: int = 20) -> bytes:
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content

def fetch_qqq_symbols() -> pd.Series:
    """
    Fetch current QQQ constituents (tickers) from Invesco.
    Tries CSV download endpoint; falls back to HTML table scrape.
    Returns pandas Series of tickers.
    """
    candidates = [
        "https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=QQQ&action=download",
        "https://www.invesco.com/us/financial-products/etfs/holdings?ticker=QQQ&audienceType=Investor&action=download",
    ]
    for url in candidates:
        try:
            content = try_download(url)
            if b"Ticker" in content or b"Symbol" in content or b"ticker" in content:
                df = pd.read_csv(io.BytesIO(content))
                for col in ["Ticker", "Symbol", "ticker", "symbol"]:
                    if col in df.columns:
                        syms = df[col].astype(str).str.strip().str.upper()
                        return syms.dropna().drop_duplicates()
                possible = [c for c in df.columns if "ick" in c.lower() or "sym" in c.lower()]
                if possible:
                    syms = df[possible[0]].astype(str).str.strip().str.upper()
                    return syms.dropna().drop_duplicates()
        except Exception:
            pass

    html_pages = [
        "https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=QQQ",
        "https://www.invesco.com/us/financial-products/etfs/holdings?ticker=QQQ&audienceType=Investor",
    ]
    for url in html_pages:
        try:
            tables = pd.read_html(url)
            for tbl in tables:
                for col in tbl.columns:
                    if str(col).strip().lower() in ("ticker", "symbol"):
                        syms = tbl[col].astype(str).str.strip().str.upper()
                        return syms.dropna().drop_duplicates()
        except Exception:
            continue

    raise RuntimeError("Failed to fetch QQQ constituents from Invesco. Provide --tickers-csv as a fallback.")

def load_extra_tickers(path: str) -> pd.Series:
    df = pd.read_csv(path)
    for col in df.columns:
        if str(col).lower() in ("ticker", "symbol", "tickers", "symbols"):
            return df[col].astype(str).str.strip().str.upper().dropna().drop_duplicates()
    if df.shape[1] == 1 and df.columns[0].startswith("Unnamed"):
        return df.iloc[:, 0].astype(str).str.strip().str.upper().dropna().drop_duplicates()
    raise RuntimeError(f"Could not find tickers column in {path}")

# ------------------------------
# Symbol mapping to Stooq format
# ------------------------------

def to_stooq_symbol(ticker: str) -> str:
    t = ticker.strip().upper()
    special = {"BRK.B": "BRK-B", "BRK B": "BRK-B", "BF.B": "BF-B", "BF B": "BF-B"}
    t = special.get(t, t)
    t = t.replace(".", "-")
    return f"{t}.US"

def from_stooq_symbol(stooq_symbol: str) -> str:
    s = stooq_symbol.upper().removesuffix(".US")
    s = s.replace("-", ".")
    return s

# ------------------------------
# Extract closes from Stooq ZIP
# ------------------------------

def extract_closes_for_symbols(zf: zipfile.ZipFile, symbols_map: dict[str, str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
    zindex_lower = {p.lower(): p for p in zf.namelist()}
    results = []
    missing = []
    
    print(f"[DEBUG] Date range: {start_date} to {end_date}", file=sys.stderr)
    print(f"[DEBUG] Total files in ZIP: {len(zf.namelist())}", file=sys.stderr)
    
    # Show sample of files in ZIP for debugging
    sample_files = [f for f in zf.namelist()[:10] if f.endswith(('.csv', '.txt'))]
    if sample_files:
        print(f"[DEBUG] Sample files in ZIP: {sample_files[:5]}", file=sys.stderr)
    
    print(f"[DEBUG] Processing {len(symbols_map)} symbols...", file=sys.stderr)

    for orig_tkr, stq_sym in symbols_map.items():
        lower_suffix_csv = f"/{stq_sym.lower()}.csv"
        lower_suffix_txt = f"/{stq_sym.lower()}.txt"
        found_path = None
        for lower_path, real_path in zindex_lower.items():
            if lower_path.endswith(lower_suffix_csv) or lower_path.endswith(lower_suffix_txt):
                found_path = real_path
                break

        if not found_path:
            missing.append(orig_tkr)
            # Show first few missing files for debugging
            if len(missing) <= 3:
                print(f"[DEBUG] Missing: {orig_tkr} -> looking for {stq_sym.lower()}.csv or .txt", file=sys.stderr)
            continue

        if len(results) < 3:  # Debug first few successful files
            print(f"[DEBUG] Found: {orig_tkr} -> {found_path}", file=sys.stderr)

        try:
            with zf.open(found_path) as f:
                df = pd.read_csv(f)
        except UnicodeDecodeError:
            with zf.open(found_path) as f:
                data = f.read().decode('latin-1')
            df = pd.read_csv(io.StringIO(data))

        # Clean up column names and find date/close columns
        df.columns = [c.strip() for c in df.columns]
        
        # Look for date column (case-insensitive, handles <date> format)
        date_col = None
        for col in df.columns:
            col_clean = col.lower().strip('<>')
            if col_clean in ('date', 'dt'):
                date_col = col
                break
        
        # Look for close column (case-insensitive, handles <close> format)  
        close_col = None
        for col in df.columns:
            col_clean = col.lower().strip('<>')
            if col_clean in ('close', 'cl'):
                close_col = col
                break
                
        if not date_col or not close_col:
            print(f"[WARN] Could not find date/close columns for {orig_tkr} in {found_path}: {df.columns}", file=sys.stderr)
            continue

        if len(results) < 3:  # Debug first few files
            print(f"[DEBUG] {orig_tkr}: Found columns date='{date_col}', close='{close_col}'", file=sys.stderr)
            print(f"[DEBUG] {orig_tkr}: Raw data shape before filtering: {df.shape}", file=sys.stderr)
            print(f"[DEBUG] {orig_tkr}: Sample date values: {df[date_col].head(3).tolist()}", file=sys.stderr)

        # Convert Stooq date format (YYYYMMDD integers) to datetime
        try:
            # First try treating as YYYYMMDD integers
            df[date_col] = pd.to_datetime(df[date_col].astype(str), format='%Y%m%d', errors='coerce')
        except:
            # Fallback to default parsing
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=False)
        
        df = df.dropna(subset=[date_col])
        
        if len(results) < 3:  # Debug date filtering
            print(f"[DEBUG] {orig_tkr}: After date parsing: {df.shape}", file=sys.stderr)
            if len(df) > 0:
                print(f"[DEBUG] {orig_tkr}: Date range in file: {df[date_col].min()} to {df[date_col].max()}", file=sys.stderr)
        
        mask = (df[date_col] >= pd.Timestamp(start_date)) & (df[date_col] <= pd.Timestamp(end_date))
        df = df.loc[mask, [date_col, close_col]].copy()
        
        if len(results) < 3:  # Debug final filtering
            print(f"[DEBUG] {orig_tkr}: After date range filtering: {df.shape}", file=sys.stderr)
        
        if len(df) == 0:
            print(f"[WARN] No data in date range for {orig_tkr}", file=sys.stderr)
            continue
            
        df.rename(columns={date_col: "date", close_col: "close"}, inplace=True)
        df["ticker"] = orig_tkr.upper()
        results.append(df)

    if missing:
        print(f"[INFO] Missing {len(missing)} tickers in Stooq bundle (examples): {', '.join(list(missing)[:10])}", file=sys.stderr)

    if not results:
        raise RuntimeError("No matching symbols were found in the Stooq ZIP. Check your ZIP file and tickers.")

    out = pd.concat(results, ignore_index=True)
    out.sort_values(["ticker", "date"], inplace=True)
    return out

# ------------------------------
# Main CLI
# ------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Extract last N years of daily closes from Stooq US daily ZIP for current S&P 500 and QQQ constituents.")
    p.add_argument("--stooq-zip", type=str, required=True, help="Path to the Stooq U.S. daily ZIP (bulk ASCII daily).")
    p.add_argument("--years", type=int, default=10, help="Number of years of history to keep (default: 10).")
    p.add_argument("--output", type=str, default=None, help="Output CSV path (default: sp500_qqq_daily_closes_LAST{years}Y.csv).")
    p.add_argument("--include", type=str, default="sp500,qqq", help="Which universes to include: comma-separated subset of {sp500, qqq}. Default: both.")
    p.add_argument("--tickers-csv", type=str, default=None, help="Optional CSV of extra tickers to include (column named 'Ticker' or 'Symbol'; or a 1-column CSV).")
    p.add_argument("--asof", type=str, default=None, help="As-of date (YYYY-MM-DD). Default: today.")
    return p.parse_args()

def main():
    args = parse_args()

    include = {x.strip().lower() for x in args.include.split(",") if x.strip()}
    if not include.issubset({"sp500", "qqq"}):
        raise SystemExit("--include must be a subset of: sp500, qqq")

    asof = datetime.strptime(args.asof, "%Y-%m-%d").date() if args.asof else datetime.today().date()
    start_date = asof - relativedelta(years=args.years)

    tickers = pd.Series(dtype=str)
    if "sp500" in include:
        print("[INFO] Fetching S&P 500 constituents from Wikipedia...", file=sys.stderr)
        sp = fetch_sp500_symbols()
        tickers = pd.concat([tickers, sp], ignore_index=True)
    if "qqq" in include:
        print("[INFO] Fetching QQQ constituents from Invesco...", file=sys.stderr)
        q = fetch_qqq_symbols()
        tickers = pd.concat([tickers, q], ignore_index=True)

    if args.tickers_csv:
        print(f"[INFO] Loading extra tickers from {args.tickers_csv}...", file=sys.stderr)
        extra = load_extra_tickers(args.tickers_csv)
        tickers = pd.concat([tickers, extra], ignore_index=True)

    tickers = tickers.dropna().astype(str).str.upper().str.strip().drop_duplicates()
    print(f"[INFO] Universe size (unique tickers): {len(tickers)}", file=sys.stderr)

    sym_map = {t: to_stooq_symbol(t) for t in tickers}

    if not os.path.exists(args.stooq_zip):
        raise SystemExit(f"Stooq ZIP not found: {args.stooq_zip}")
    print(f"[INFO] Opening Stooq ZIP: {args.stooq_zip}", file=sys.stderr)
    with zipfile.ZipFile(args.stooq_zip, "r") as zf:
        df = extract_closes_for_symbols(zf, sym_map, start_date, asof)

    out_path = args.output or f"sp500_qqq_daily_closes_LAST{args.years}Y.csv"
    df.to_csv(out_path, index=False)
    print(f"[DONE] Wrote {len(df):,} rows to {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
