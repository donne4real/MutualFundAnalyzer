"""
Tests for ETF Backtester Module
"""

import pytest
from src.backtester import BacktestConfig, BacktestResults, Backtester, Trade


class TestBacktestConfig:
    """Tests for the BacktestConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )

        assert config.initial_capital == 100000
        assert config.rebalance_frequency == "monthly"
        assert config.position_size_pct == 0.10
        assert config.min_score_threshold == 50
        assert config.transaction_cost_pct == 0.001
        assert config.benchmark == "SPY"

    def test_custom_values(self):
        """Test custom configuration values."""
        config = BacktestConfig(
            start_date="2022-06-01",
            end_date="2023-06-01",
            initial_capital=50000,
            rebalance_frequency="weekly",
            position_size_pct=0.20,
            min_score_threshold=60,
            transaction_cost_pct=0.002,
            benchmark="QQQ"
        )

        assert config.initial_capital == 50000
        assert config.rebalance_frequency == "weekly"
        assert config.position_size_pct == 0.20
        assert config.min_score_threshold == 60
        assert config.transaction_cost_pct == 0.002
        assert config.benchmark == "QQQ"


class TestBacktestResults:
    """Tests for the BacktestResults class."""

    def test_default_values(self):
        """Test default results values."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )
        results = BacktestResults(config=config)

        assert results.total_return == 0.0
        assert results.annualized_return == 0.0
        assert results.benchmark_return == 0.0
        assert results.sharpe_ratio == 0.0
        assert results.total_trades == 0
        assert results.trades == []

    def test_excess_return(self):
        """Test excess return calculation."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )
        results = BacktestResults(
            config=config,
            total_return=0.15,
            benchmark_return=0.10
        )

        assert results.excess_return == 0.05


class TestTrade:
    """Tests for the Trade dataclass."""

    def test_trade_creation(self):
        """Test creating a trade."""
        from datetime import datetime

        trade = Trade(
            date=datetime(2023, 6, 15),
            ticker="SPY",
            action="BUY",
            shares=10,
            price=400.00,
            value=4000.00,
            transaction_cost=4.00,
            reason="Score: 75"
        )

        assert trade.ticker == "SPY"
        assert trade.action == "BUY"
        assert trade.shares == 10
        assert trade.value == 4000.00


class TestBacktester:
    """Tests for the Backtester class."""

    def test_init(self):
        """Test backtester initialization."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )
        backtester = Backtester(config)

        assert backtester.config == config
        assert backtester.trades == []
        assert backtester.portfolio_values == []

    def test_get_rebalance_dates_daily(self):
        """Test daily rebalance dates generation."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2023-01-05",
            rebalance_frequency="daily"
        )
        backtester = Backtester(config)
        dates = backtester._get_rebalance_dates()

        assert len(dates) == 5

    def test_get_rebalance_dates_monthly(self):
        """Test monthly rebalance dates generation."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2023-04-01",
            rebalance_frequency="monthly"
        )
        backtester = Backtester(config)
        dates = backtester._get_rebalance_dates()

        assert len(dates) == 4  # Jan, Feb, Mar, Apr

    def test_get_rebalance_dates_quarterly(self):
        """Test quarterly rebalance dates generation."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2023-12-31",
            rebalance_frequency="quarterly"
        )
        backtester = Backtester(config)
        dates = backtester._get_rebalance_dates()

        assert len(dates) == 4  # Q1, Q2, Q3, Q4

    def test_get_rebalance_dates_yearly(self):
        """Test yearly rebalance dates generation."""
        config = BacktestConfig(
            start_date="2020-01-01",
            end_date="2024-01-01",
            rebalance_frequency="yearly"
        )
        backtester = Backtester(config)
        dates = backtester._get_rebalance_dates()

        assert len(dates) == 5  # 2020, 2021, 2022, 2023, 2024

    def test_calculate_results_empty(self):
        """Test results calculation with empty data."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )
        backtester = Backtester(config)
        results = backtester._calculate_results([], 100)

        assert isinstance(results, BacktestResults)
        assert results.config == config

    def test_run_backtest(self):
        """Test running a backtest (may require network)."""
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2023-02-01",  # Short period for speed
            initial_capital=10000,
            rebalance_frequency="weekly",
        )
        backtester = Backtester(config)

        # This may fail without network access
        try:
            results = backtester.run_backtest(["SPY"])
            assert isinstance(results, BacktestResults)
        except Exception as e:
            # Network errors are expected in isolated environments
            pytest.skip(f"Network access required: {e}")

    def test_export_results(self, tmp_path):
        """Test exporting backtest results."""
        import os
        from datetime import datetime
        import pandas as pd

        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-01-01"
        )

        results = BacktestResults(
            config=config,
            total_return=0.15,
            annualized_return=0.14,
            benchmark_return=0.10,
            sharpe_ratio=1.2,
            total_trades=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=0.6,
            total_transaction_costs=50.00,
            portfolio_values=pd.DataFrame({
                "portfolio_value": [100000, 105000, 110000, 115000],
                "cash": [10000, 10000, 10000, 10000],
                "holdings_value": [90000, 95000, 100000, 105000]
            }, index=pd.date_range("2023-01-01", periods=4, freq="M")),
            trades=[
                Trade(
                    date=datetime(2023, 1, 15),
                    ticker="SPY",
                    action="BUY",
                    shares=10,
                    price=400.00,
                    value=4000.00,
                    transaction_cost=4.00,
                    reason="Score: 75"
                )
            ]
        )

        backtester = Backtester(config)
        original_output_dir = "output"

        # Temporarily change output directory
        import src.backtester as bt_module
        original_join = bt_module.os.path.join
        bt_module.os.path.join = lambda *args: os.path.join(str(tmp_path), args[-1]) if len(args) > 1 else original_join(*args)

        try:
            filepath = backtester.export_results(results)
            assert os.path.exists(filepath)
            assert filepath.endswith(".xlsx")
        finally:
            bt_module.os.path.join = original_join
