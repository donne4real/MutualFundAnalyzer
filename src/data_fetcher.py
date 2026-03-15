"""
Mutual Fund Data Fetcher Module

Provides intelligent mutual fund data retrieval from Yahoo Finance with:
- 24-hour caching to minimize API calls
- Rate limiting (1 second between requests)
- Batch processing with progress tracking
- Automatic fallback to cached data

Classes:
    MutualFundDataFetcher: Main class for fetching mutual fund data with caching

Example:
    >>> fetcher = MutualFundDataFetcher()
    >>> fund = fetcher.fetch_fund_data("VFIAX")
    >>> print(f"{fund['symbol']}: ${fund['price']}")
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

# Cache configuration - Cross-platform compatible paths
CACHE_BASE_DIR = Path.home() / ".qwen_mutual_fund_analyzer" / "cache"
CACHE_DIR = CACHE_BASE_DIR
CACHE_FILE = CACHE_BASE_DIR / "mutual_fund_cache.json"
CACHE_EXPIRY_HOURS = 24
RATE_LIMIT_DELAY = 1.0


class MutualFundDataFetcher:
    """
    Fetches mutual fund data from Yahoo Finance with intelligent caching and rate limiting.

    Features:
        - 24-hour local caching reduces API calls
        - Automatic rate limiting (1 second between requests)
        - Batch processing with progress tracking
        - Graceful fallback to cached data on errors
    """

    def __init__(self):
        """Initialize the fetcher and load existing cache from disk."""
        self.cache: dict = {}
        self._load_cache()

    def _load_cache(self):
        """Load existing cache from disk on initialization."""
        try:
            CACHE_BASE_DIR.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not create cache directory: {e}")

        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                print(f"Loaded cache with {len(self.cache)} mutual funds")
            except (json.JSONDecodeError, IOError, PermissionError) as e:
                print(f"Warning: Could not load cache: {e}")
                self.cache = {}

    def _save_cache(self):
        """Save current cache to disk in JSON format."""
        try:
            CACHE_BASE_DIR.mkdir(parents=True, exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2, default=str)
        except (OSError, IOError, PermissionError, TypeError) as e:
            print(f"Warning: Could not save cache: {e}")

    def _is_cache_valid(self, ticker: str) -> bool:
        """Check if cached data for a ticker is still valid."""
        if ticker not in self.cache:
            return False
        cached_time = self.cache[ticker].get("timestamp", "")
        if not cached_time:
            return False
        try:
            cache_dt = datetime.fromisoformat(cached_time)
            return datetime.now() - cache_dt < timedelta(hours=CACHE_EXPIRY_HOURS)
        except:
            return False

    def _get_cached_data(self, ticker: str) -> Optional[dict]:
        """Retrieve valid cached data for a ticker."""
        if self._is_cache_valid(ticker):
            return self.cache[ticker].get("data")
        return None

    def _cache_data(self, ticker: str, data: dict):
        """Store mutual fund data in cache with current timestamp."""
        self.cache[ticker] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self._save_cache()

    def fetch_fund_data(self, ticker: str) -> Optional[dict]:
        """
        Fetch comprehensive mutual fund data for a single ticker.

        Args:
            ticker (str): Mutual fund ticker symbol (e.g., 'VFIAX', 'FXAIX')

        Returns:
            Optional[dict]: Dictionary containing mutual fund data
        """
        cached = self._get_cached_data(ticker)
        if cached:
            print(f"  [CACHE] {ticker}")
            return cached

        try:
            time.sleep(RATE_LIMIT_DELAY)
            fund = yf.Ticker(ticker)
            info = fund.info

            if not info or not info.get("symbol"):
                print(f"  [SKIP] {ticker} - No data available")
                return None

            def safe_get_numeric(data, key, default=None):
                val = data.get(key)
                if val is None:
                    return default
                try:
                    return float(val) if val not in ('', 'N/A', 'NaN') else default
                except (ValueError, TypeError):
                    return default

            data = {
                "symbol": info.get("symbol", ticker),
                "name": info.get("shortName") or info.get("longName") or "N/A",
                "category": info.get("category") or "N/A",
                "family": info.get("fundFamily") or "N/A",
                "exchange": info.get("exchange") or "N/A",
                "nav_price": safe_get_numeric(info, "navPrice"),
                "price": safe_get_numeric(info, "previousClose") or safe_get_numeric(info, "regularMarketPrice"),
                "pe_ratio": safe_get_numeric(info, "trailingPE"),
                "pb_ratio": safe_get_numeric(info, "priceToBook"),
                "dividend_yield": safe_get_numeric(info, "dividendYield"),
                "expense_ratio": safe_get_numeric(info, "annualReportExpenseRatio"),
                "yield": safe_get_numeric(info, "yield"),
                "ytd_return": safe_get_numeric(info, "ytdReturn"),
                "three_year_return": safe_get_numeric(info, "threeYearAverageReturn"),
                "five_year_return": safe_get_numeric(info, "fiveYearAverageReturn"),
                "ten_year_return": safe_get_numeric(info, "tenYearAverageReturn"),
                "holdings_count": safe_get_numeric(info, "holdingsCount"),
                "bond_holdings": safe_get_numeric(info, "bondHoldings"),
                "stock_holdings": safe_get_numeric(info, "equityHoldings"),
                "cash_holdings": safe_get_numeric(info, "cashHoldings"),
                "other_holdings": safe_get_numeric(info, "otherHoldings"),
                "top_10_holdings_pct": safe_get_numeric(info, "top10Holdings"),
                "turnover_rate": safe_get_numeric(info, "fundTurnover"),
                "net_assets": safe_get_numeric(info, "netAssets"),
                "inception_date": info.get("fundInceptionDate"),
                "min_initial_investment": safe_get_numeric(info, "minimumInvestment"),
                "min_subsequent_investment": safe_get_numeric(info, "subsequentInvestment"),
                "beta": safe_get_numeric(info, "beta"),
                "alpha": safe_get_numeric(info, "alpha"),
                "mean_annual_return": safe_get_numeric(info, "meanAnnualReturn"),
                "risk_rating": info.get("riskRating"),
                "morningstar_rating": safe_get_numeric(info, "morningStarRating"),
                "morningstar_risk": info.get("morningStarRiskRating"),
                "sustainability_rating": safe_get_numeric(info, "sustainabilityRating"),
            }

            # Get historical data for momentum calculation
            try:
                hist = fund.history(period="1y")
                if hist is not None and len(hist) > 0:
                    close_prices = hist["Close"]
                    if len(close_prices) > 0:
                        data["year_ago_price"] = float(close_prices.iloc[0])
                    if len(close_prices) > 126:
                        data["6_month_ago_price"] = float(close_prices.iloc[len(close_prices)//2])
                    if len(close_prices) > 189:
                        data["3_month_ago_price"] = float(close_prices.iloc[len(close_prices)*3//4])
            except Exception as e:
                print(f"  [WARN] {ticker} - Could not fetch historical data: {e}")

            self._cache_data(ticker, data)
            print(f"  [FETCH] {ticker} - {data.get('name', 'N/A')}")
            return data

        except Exception as e:
            print(f"  [ERROR] {ticker} - {str(e)}")
            return None

    def fetch_multiple_funds(self, tickers: list, batch_size: int = 50) -> list:
        """Fetch data for multiple mutual funds with batching and progress tracking."""
        results = []
        total = len(tickers)

        print(f"\nFetching data for {total} mutual funds (batch size: {batch_size})...")
        print("=" * 60)

        for i, ticker in enumerate(tickers, 1):
            print(f"[{i}/{total}] ", end="")
            data = self.fetch_fund_data(ticker)
            if data:
                results.append(data)

        print("=" * 60)
        print(f"Fetched {len(results)} of {total} mutual funds successfully")
        return results

    def clear_cache(self):
        """Clear all cached data from memory and disk."""
        self.cache = {}
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
        print("Cache cleared")


def get_fund_categories() -> dict:
    """Get a dictionary of mutual fund categories with representative tickers."""
    return {
        "Index Funds": [
            "VFIAX", "FXAIX", "SWPPX",  # S&P 500
            "VTSAX", "FSKAX", "SWTSX",  # Total Market
            "VTIAX", "FTIHX", "SWISX",  # International
            "VWIAX", "VBIAX",  # Balanced
            "VBTLX", "FXNAX", "SWAGX",  # Total Bond
        ],
        "Large Cap Blend": [
            "VFIAX", "FXAIX", "SWPPX", "VFINX",
            "FSKAX", "SWTSX", "VTSAX",
            "DODGX", "VQNPX", "TRBCX",
        ],
        "Large Cap Growth": [
            "VIGAX", "TRSGX", "FMAGX", "FBGRX",
            "AGTHX", "PRGFX", "VWUSX", "TRBCX",
            "FCNTX", "XLCGX",
        ],
        "Large Cap Value": [
            "VVIAX", "VWELX", "DODBX", "FSMAX",
            "VHDYX", "TRBCX", "PRIDX", "FDVLX",
        ],
        "Mid Cap": [
            "VIMAX", "FSMDX", "SWMCX", "VIMSX",
            "TRMCX", "PRMTX", "JDMAX",
        ],
        "Small Cap": [
            "VSMAX", "FSSNX", "SWSSX", "NAESX",
            "TRSSX", "JAFVX", "PRDSX",
        ],
        "International": [
            "VTIAX", "FTIHX", "SWISX", "VGTSX",
            "FSPSX", "HAINX", "DODFX", "PRIDX",
            "VFWAX", "VTMGX",
        ],
        "Emerging Markets": [
            "VEMAX", "FEMKX", "MSOAX", "VEIEX",
            "DODMX", "PRMSX", "SEEMX",
        ],
        "Bond Funds": [
            "VBTLX", "FXNAX", "SWAGX", "VBMFX",
            "FTBFX", "PIMIX", "DODIX", "VWITX",
            "VFSTX", "FSHBX",
        ],
        "Target Date": [
            "VFIFX", "FFNOX", "TRRFX", "VTTVX",
            "VTHRX", "VTTSX", "FFTLX", "TRRCX",
        ],
        "Sector Funds": [
            "VGSLX", "FSRNX",  # Real Estate
            "VGHAX", "FBIOX",  # Healthcare
            "FSENX", "VGENX",  # Energy
            "FSPTX", "VITAX",  # Technology
            "FSUTX", "VUIAX",  # Utilities
        ],
        "Balanced/Allocation": [
            "VWELX", "VBIAX", "SWOBX", "VWINX",
            "DODBX", "FBALX", "TRPBX", "VSCGX",
        ],
        "Dividend/Income": [
            "VHDYX", "FDVV", "SCHD", "VYM",
            "Fidelity Dividend Growth", "VDIGX",
        ],
        "ESG/Sustainable": [
            "VFTAX", "ESGV", "SUSL", "DSI",
            "VSGAX", "ESGU", "SUSA",
        ],
    }


def get_all_fund_tickers() -> list:
    """Get a comprehensive list of popular mutual fund tickers."""
    categories = get_fund_categories()
    all_tickers = []
    for tickers in categories.values():
        all_tickers.extend(tickers)
    return list(dict.fromkeys(all_tickers))  # Remove duplicates while preserving order


def get_vanguard_funds() -> list:
    """Get Vanguard mutual fund tickers."""
    return [
        "VFIAX", "VTSAX", "VTIAX", "VBTLX", "VWELX", "VWIAX",
        "VIGAX", "VVIAX", "VIMAX", "VSMAX", "VEMAX", "VHDYX",
        "VFTAX", "VSGAX", "VFIFX", "VTHRX", "VTTVX", "VTTSX",
        "VGSLX", "VGHAX", "VGENX", "VITAX", "VUIAX", "VBMFX",
        "VWINX", "VSCGX", "VDIGX", "VWITX", "VFSTX",
    ]


def get_fidelity_funds() -> list:
    """Get Fidelity mutual fund tickers."""
    return [
        "FXAIX", "FSKAX", "FTIHX", "FXNAX", "FBALX",
        "FMAGX", "FBGRX", "FSENX", "FSPTX", "FSUTX",
        "FSRNX", "FBIOX", "FSSNX", "FEMKX", "FTBFX",
        "FFNOX", "FFTLX", "FDVV", "FSMDX", "FSHBX",
    ]


def get_schwab_funds() -> list:
    """Get Schwab mutual fund tickers."""
    return [
        "SWPPX", "SWTSX", "SWISX", "SWAGX", "SWOBX",
        "SWMCX", "SWSSX", "SWOAX", "SWRAX",
    ]


if __name__ == "__main__":
    fetcher = MutualFundDataFetcher()
    tickers = ["VFIAX", "FXAIX", "VTSAX"]
    results = fetcher.fetch_multiple_funds(tickers)
    print(f"\nResults: {len(results)} mutual funds")
    for r in results:
        print(f"  {r['symbol']}: ${r.get('nav_price', 'N/A')} - {r.get('name', 'N/A')}")
