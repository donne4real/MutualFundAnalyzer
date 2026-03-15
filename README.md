# 📈 Mutual Fund Analyzer

A comprehensive mutual fund analysis application that evaluates mutual funds using **10 sophisticated investment models** and exports results to Excel. Includes **backtesting functionality** to test strategies on historical data.

## Features

### Mutual Fund Analysis
- **10 Investment Models:**
  1. **Cost Efficiency** - Low expense ratio, turnover, minimum investment
  2. **Performance Score** - 10Y, 5Y, 3Y, YTD returns
  3. **Manager Quality** - Fund family reputation, track record, fund size
  4. **Risk-Adjusted Return** - Alpha, beta, Morningstar risk rating
  5. **Diversification Score** - Holdings count, concentration
  6. **Tax Efficiency** - Turnover rate, fund structure
  7. **Fund Quality** - Morningstar rating, sustainability rating
  8. **Growth Score** - Long-term growth trajectory
  9. **Income Score** - Dividend yield, distribution consistency
  10. **ESG Score** - Environmental, Social, Governance factors

- **Fund Category Filters:**
  - Index Funds (VFIAX, VTSAX, FXAIX, etc.)
  - Large Cap Blend/Growth/Value
  - Mid Cap & Small Cap
  - International & Emerging Markets
  - Bond Funds
  - Target Date Funds
  - Sector Funds
  - Balanced/Allocation Funds
  - Dividend/Income Funds
  - ESG/Sustainable Funds

- **Fund Family Coverage:**
  - Vanguard (VFIAX, VTSAX, VBTLX, etc.)
  - Fidelity (FXAIX, FSKAX, FBALX, etc.)
  - Schwab (SWPPX, SWTSX, SWAGX, etc.)
  - T. Rowe Price, American Funds, PIMCO, and more

- **Web Interface:** Clean Streamlit UI with Morningstar ratings
- **Rate Limit Handling:** Intelligent caching (24h) + rate limiting
- **Excel Export:** Formatted spreadsheets with color-coded scores
- **Custom Tickers:** Analyze your own fund selections

### Backtesting
- **Historical Simulation** - Test strategies on historical data
- **Configurable Parameters:**
  - Date range selection
  - Initial capital
  - Rebalance frequency (daily, weekly, monthly, quarterly, yearly)
  - Position sizing
  - Minimum score threshold
  - Transaction costs
  - Benchmark comparison (SPY, VOO, VTI, BND)
- **Performance Metrics:**
  - Total return & annualized return
  - Sharpe ratio & Sortino ratio
  - Maximum drawdown
  - Beta & Alpha
  - Win rate & trade statistics
- **Visualizations** - Portfolio growth charts and comparison tables
- **Export Results** - Download backtest results to Excel

## Installation

```bash
# Navigate to project directory
cd MutualFundAnalyzer

# Install dependencies
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- yfinance >= 0.2.31
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- streamlit >= 1.28.0
- numpy >= 1.24.0
- pytest >= 7.4.0 (for testing)

## Usage

### Web Interface (Recommended)

```bash
# Run the Streamlit app
streamlit run app.py
```

This opens a web interface at `http://localhost:8501` where you can:

**Fund Analysis Page:**
1. Select fund category (Index Funds, Large Cap, Bond, etc.) or enter custom tickers
2. Click "Run Analysis"
3. View results with Morningstar ratings and charts
4. Export to Excel or CSV

**Backtesting Page:**
1. Set date range
2. Configure initial capital
3. Choose rebalance frequency
4. Set position sizing and quality thresholds
5. Select benchmark for comparison
6. Click "Run Backtest"
7. View performance metrics and charts
8. Export results to Excel

### CLI Mode (Test Fetcher)

```bash
python src/data_fetcher.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_strategies.py -v
```

## Project Structure

```
MutualFundAnalyzer/
├── app.py                 # Streamlit web interface
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py   # Mutual fund data with caching
│   ├── strategies.py     # 10 investment models
│   ├── exporter.py       # Excel/CSV export
│   └── backtester.py     # Historical backtesting
├── tests/
│   ├── __init__.py
│   ├── test_strategies.py
│   ├── test_data_fetcher.py
│   ├── test_exporter.py
│   └── test_backtester.py
├── cache/                # Auto-created cache directory
└── output/               # Exported spreadsheets
```

## How It Works

### Rate Limit Workaround

1. **Caching:** Mutual fund data cached for 24 hours in user's home directory
2. **Rate Limiting:** 1 second delay between requests
3. **Batch Processing:** Fetches in batches of 50 with progress tracking
4. **Fallback:** Uses cached data if API fails

### Cross-Platform Cache

The cache is stored in the user's home directory:
- **Windows:** `C:\Users\<user>\.qwen_mutual_fund_analyzer\cache\`
- **Linux/Mac:** `~/.qwen_mutual_fund_analyzer/cache/`

### Scoring System

Each model scores funds from **0-10**:
- 🟢 **8-10:** Strong buy signal
- 🟡 **5-7:** Moderate/hold
- 🔴 **0-4:** Weak/avoid

Total score = sum of all 10 models (max 100)

## Model Details

### Cost Efficiency
Evaluates fund costs:
- Expense ratio (max 5 points)
- Turnover rate (max 1 point)
- Minimum investment (max 1 point)

### Performance Score
Measures historical returns:
- 10-year return (max 4 points)
- 5-year return (max 3 points)
- 3-year return (max 2 points)
- YTD return (max 1 point)

### Manager Quality
Assesses fund management:
- Fund family reputation (max 4 points)
- Fund age/track record (max 3 points)
- Net assets (max 2 points)

### Risk-Adjusted Return
Evaluates risk metrics:
- Alpha (max 4 points)
- Beta (max 2 points)
- Morningstar risk rating (max 3 points)
- Mean annual return (max 1 point)

### Diversification Score
Measures portfolio spread:
- Holdings count (max 4 points)
- Top 10 concentration (max 3 points)
- Asset allocation (max 2 points)

### Tax Efficiency
Evaluates tax impact:
- Turnover rate (lower = better)
- Index vs active management
- ETF structure bonus

### Fund Quality
Assesses overall quality:
- Morningstar rating (max 4 points)
- Sustainability rating (max 2 points)
- Risk rating (max 1 point)

### Growth Score
Measures growth potential:
- Long-term consistency
- 10-year growth trajectory
- Recent momentum

### Income Score
Evaluates income generation:
- Dividend/fund yield (max 4 points)
- Category bonus for income funds
- Bond allocation bonus

### ESG Score
Assesses sustainability:
- Sustainability rating (max 4 points)
- ESG focus identification (max 3 points)

## Popular Funds by Category

### Index Funds
| Ticker | Name | Expense Ratio |
|--------|------|---------------|
| VFIAX | Vanguard 500 Index | 0.04% |
| FXAIX | Fidelity 500 Index | 0.015% |
| SWPPX | Schwab S&P 500 Index | 0.02% |
| VTSAX | Vanguard Total Stock Market | 0.04% |
| FSKAX | Fidelity Total Market Index | 0.015% |

### Bond Funds
| Ticker | Name | Expense Ratio |
|--------|------|---------------|
| VBTLX | Vanguard Total Bond Market | 0.05% |
| FXNAX | Fidelity US Bond Index | 0.025% |
| SWAGX | Schwab US Aggregate Bond | 0.04% |

### Target Date Funds
| Ticker | Name | Target Year |
|--------|------|-------------|
| VFIFX | Vanguard Target Retirement 2050 | 2050 |
| VTHRX | Vanguard Target Retirement 2030 | 2030 |
| FFNOX | Fidelity Freedom 2040 | 2040 |

### Balanced Funds
| Ticker | Name | Stock/Bond |
|--------|------|------------|
| VWELX | Vanguard Wellington | ~65/35 |
| VWINX | Vanguard Wellesley Income | ~40/60 |
| FBALX | Fidelity Balanced | ~60/40 |

## Configuration

Edit these values in `src/data_fetcher.py`:

```python
CACHE_EXPIRY_HOURS = 24  # Cache validity
RATE_LIMIT_DELAY = 1.0   # Seconds between requests
```

## Example Output

The Excel spreadsheet includes:
- **Summary Sheet:** Top 50 funds with scores and recommendations
- **Details Sheet:** All metrics for each fund
- **Statistics Sheet:** Score distributions and strategy averages
- **Strategy Scores Sheet:** Individual strategy scores for each fund
- **Family Analysis:** Fund family comparison

Color coding:
- 🟢 Green: High scores (8-10)
- 🟡 Amber: Medium scores (5-7)
- 🔴 Red: Low scores (0-4)

## Morningstar Ratings

The analyzer displays Morningstar ratings when available:
- ⭐⭐⭐⭐⭐ (5 stars) - Top 10%
- ⭐⭐⭐⭐ (4 stars) - Next 22.5%
- ⭐⭐⭐ (3 stars) - Middle 35%
- ⭐⭐ (2 stars) - Next 22.5%
- ⭐ (1 star) - Bottom 10%

## Disclaimer

⚠️ **For educational purposes only.** This is not financial advice. Always do your own research before making investment decisions. Past performance does not guarantee future results. Mutual fund investments involve risk including possible loss of principal.

## License

MIT License

## Changelog

### Version 1.0.0
- Initial release with 10 investment models for mutual funds
- Mutual fund analysis UI with category filters
- Excel/CSV export with color coding
- Comprehensive backtesting module
- Support for 100+ popular mutual funds
- Morningstar rating integration
- Cross-platform caching
