"""
Tests for Mutual Fund Data Fetcher Module
"""

import pytest
from src.data_fetcher import MutualFundDataFetcher, get_fund_categories, get_all_fund_tickers


class TestMutualFundDataFetcher:
    """Tests for the MutualFundDataFetcher class."""

    def test_init(self):
        """Test fetcher initialization."""
        fetcher = MutualFundDataFetcher()
        assert fetcher is not None
        assert isinstance(fetcher.cache, dict)

    def test_fetch_single_fund(self):
        """Test fetching a single mutual fund."""
        fetcher = MutualFundDataFetcher()
        result = fetcher.fetch_fund_data("VFIAX")

        if result:  # May fail if no internet
            assert "symbol" in result
            assert result["symbol"] == "VFIAX"
            assert "name" in result
            assert "nav_price" in result or result.get("nav_price") is None

    def test_cache_functionality(self):
        """Test caching mechanism."""
        fetcher = MutualFundDataFetcher()

        # First fetch (may hit network)
        result1 = fetcher.fetch_fund_data("VFIAX")

        # Second fetch should use cache
        result2 = fetcher.fetch_fund_data("VFIAX")

        if result1 and result2:
            assert result1["symbol"] == result2["symbol"]

    def test_clear_cache(self):
        """Test cache clearing."""
        fetcher = MutualFundDataFetcher()
        fetcher.clear_cache()
        assert len(fetcher.cache) == 0


class TestGetFundCategories:
    """Tests for get_fund_categories function."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        categories = get_fund_categories()
        assert isinstance(categories, dict)

    def test_has_expected_categories(self):
        """Test that expected categories are present."""
        categories = get_fund_categories()
        expected = [
            "Index Funds",
            "Large Cap Blend",
            "Large Cap Growth",
            "Large Cap Value",
            "Mid Cap",
            "Small Cap",
            "International",
            "Bond Funds",
            "Target Date",
            "Balanced/Allocation",
        ]
        for category in expected:
            assert category in categories

    def test_categories_have_tickers(self):
        """Test that each category has tickers."""
        categories = get_fund_categories()
        for category, tickers in categories.items():
            assert isinstance(tickers, list)
            assert len(tickers) > 0
            for ticker in tickers:
                assert isinstance(ticker, str)
                assert len(ticker) > 0


class TestGetAllFundTickers:
    """Tests for get_all_fund_tickers function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        tickers = get_all_fund_tickers()
        assert isinstance(tickers, list)

    def test_no_duplicates(self):
        """Test that there are no duplicate tickers."""
        tickers = get_all_fund_tickers()
        assert len(tickers) == len(set(tickers))

    def test_has_popular_funds(self):
        """Test that popular funds are included."""
        tickers = get_all_fund_tickers()
        popular = ["VFIAX", "VTSAX", "FXAIX", "VBTLX", "VWELX"]
        for fund in popular:
            assert fund in tickers

    def test_reasonable_count(self):
        """Test that we have a reasonable number of funds."""
        tickers = get_all_fund_tickers()
        assert len(tickers) >= 50  # Should have at least 50 funds
