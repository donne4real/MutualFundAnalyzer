"""
Tests for Mutual Fund Investment Strategies Module
"""

import pytest
from src.strategies import MutualFundStrategies, STRATEGY_NAMES


class TestCostEfficiency:
    """Tests for the Cost Efficiency strategy."""

    def test_ultra_low_expense(self):
        """Test fund with ultra-low expense ratio."""
        fund_data = {
            "expense_ratio": 0.00015,
            "turnover_rate": 0.05,
            "min_initial_investment": 0,
        }
        score, reason = MutualFundStrategies.score_cost_efficiency(fund_data)
        assert score >= 6  # Ultra-low expense + low turnover + low minimum

    def test_high_expense(self):
        """Test fund with high expense ratio."""
        fund_data = {
            "expense_ratio": 0.015,
            "turnover_rate": 0.90,
            "min_initial_investment": 50000,
        }
        score, reason = MutualFundStrategies.score_cost_efficiency(fund_data)
        assert score <= 3  # High expense penalty


class TestPerformance:
    """Tests for the Performance Score strategy."""

    def test_strong_long_term_performance(self):
        """Test fund with strong long-term returns."""
        fund_data = {
            "ten_year_return": 0.13,
            "five_year_return": 0.14,
            "three_year_return": 0.12,
            "ytd_return": 0.15,
        }
        score, reason = MutualFundStrategies.score_performance(fund_data)
        assert score >= 8  # Strong performance

    def test_weak_performance(self):
        """Test fund with weak returns."""
        fund_data = {
            "ten_year_return": 0.02,
            "five_year_return": 0.03,
            "three_year_return": 0.01,
            "ytd_return": -0.05,
        }
        score, reason = MutualFundStrategies.score_performance(fund_data)
        assert score <= 3  # Weak performance


class TestManagerQuality:
    """Tests for the Manager Quality strategy."""

    def test_top_tier_family(self):
        """Test fund from top-tier family."""
        fund_data = {
            "family": "Vanguard",
            "inception_date": 631152000,  # 1990
            "net_assets": 50e9,
        }
        score, reason = MutualFundStrategies.score_manager_quality(fund_data)
        assert score >= 7  # Top family + established + large

    def test_unknown_family(self):
        """Test fund from unknown family."""
        fund_data = {
            "family": "Unknown Fund Company",
            "inception_date": None,
            "net_assets": 50e6,
        }
        score, reason = MutualFundStrategies.score_manager_quality(fund_data)
        assert score <= 4  # Unknown family


class TestRiskAdjusted:
    """Tests for the Risk-Adjusted Return strategy."""

    def test_positive_alpha(self):
        """Test fund with positive alpha."""
        fund_data = {
            "alpha": 3.5,
            "beta": 0.95,
            "morningstar_risk": "Low",
            "mean_annual_return": 0.12,
        }
        score, reason = MutualFundStrategies.score_risk_adjusted(fund_data)
        assert score >= 8  # Excellent alpha + good beta + low risk

    def test_negative_alpha(self):
        """Test fund with negative alpha."""
        fund_data = {
            "alpha": -2.0,
            "beta": 1.4,
            "morningstar_risk": "High",
            "mean_annual_return": 0.03,
        }
        score, reason = MutualFundStrategies.score_risk_adjusted(fund_data)
        assert score <= 3  # Negative alpha + high beta + high risk


class TestDiversification:
    """Tests for the Diversification Score strategy."""

    def test_highly_diversified(self):
        """Test fund with many holdings."""
        fund_data = {
            "holdings_count": 500,
            "top_10_holdings_pct": 0.20,
            "stock_holdings": 0.60,
            "bond_holdings": 0.35,
            "cash_holdings": 0.05,
        }
        score, reason = MutualFundStrategies.score_diversification(fund_data)
        assert score >= 7  # Highly diversified

    def test_concentrated(self):
        """Test fund with few holdings."""
        fund_data = {
            "holdings_count": 25,
            "top_10_holdings_pct": 0.70,
            "stock_holdings": 1.0,
            "bond_holdings": 0,
            "cash_holdings": 0,
        }
        score, reason = MutualFundStrategies.score_diversification(fund_data)
        assert score <= 4  # Concentrated


class TestTaxEfficiency:
    """Tests for the Tax Efficiency strategy."""

    def test_index_fund(self):
        """Test index fund (tax efficient)."""
        fund_data = {
            "turnover_rate": 0.05,
            "category": "Large Blend Index",
            "name": "S&P 500 Index Fund",
        }
        score, reason = MutualFundStrategies.score_tax_efficiency(fund_data)
        assert score >= 8  # Low turnover + index fund

    def test_active_fund(self):
        """Test actively managed fund (less tax efficient)."""
        fund_data = {
            "turnover_rate": 0.85,
            "category": "Active Large Cap",
            "name": "Actively Managed Fund",
        }
        score, reason = MutualFundStrategies.score_tax_efficiency(fund_data)
        assert score <= 4  # High turnover + active


class TestFundQuality:
    """Tests for the Fund Quality strategy."""

    def test_five_star_fund(self):
        """Test 5-star Morningstar fund."""
        fund_data = {
            "morningstar_rating": 5,
            "sustainability_rating": 4,
            "risk_rating": "Low",
        }
        score, reason = MutualFundStrategies.score_fund_quality(fund_data)
        assert score >= 9  # 5-star + high sustainability + low risk

    def test_low_rated_fund(self):
        """Test low-rated fund."""
        fund_data = {
            "morningstar_rating": 2,
            "sustainability_rating": 2,
            "risk_rating": "High",
        }
        score, reason = MutualFundStrategies.score_fund_quality(fund_data)
        assert score <= 4  # Low ratings


class TestGrowth:
    """Tests for the Growth Score strategy."""

    def test_consistent_growth(self):
        """Test fund with consistent growth."""
        fund_data = {
            "ten_year_return": 0.12,
            "five_year_return": 0.14,
            "three_year_return": 0.11,
            "ytd_return": 0.18,
        }
        score, reason = MutualFundStrategies.score_growth(fund_data)
        assert score >= 8  # Consistent strong growth

    def test_inconsistent_growth(self):
        """Test fund with inconsistent growth."""
        fund_data = {
            "ten_year_return": 0.03,
            "five_year_return": -0.02,
            "three_year_return": 0.08,
            "ytd_return": -0.10,
        }
        score, reason = MutualFundStrategies.score_growth(fund_data)
        assert score <= 4  # Inconsistent/weak growth


class TestIncome:
    """Tests for the Income Score strategy."""

    def test_high_yield_fund(self):
        """Test fund with high yield."""
        fund_data = {
            "dividend_yield": 0.05,
            "category": "Bond Fund",
            "bond_holdings": 0.95,
        }
        score, reason = MutualFundStrategies.score_income(fund_data)
        assert score >= 6  # High yield + bond fund

    def test_no_yield_fund(self):
        """Test fund with no yield."""
        fund_data = {
            "dividend_yield": None,
            "category": "Growth Fund",
            "bond_holdings": 0,
        }
        score, reason = MutualFundStrategies.score_income(fund_data)
        assert score <= 3  # No yield data


class TestESG:
    """Tests for the ESG Score strategy."""

    def test_esg_fund(self):
        """Test ESG-focused fund."""
        fund_data = {
            "sustainability_rating": 5,
            "category": "ESG Large Cap",
            "name": "Sustainable Equity Fund",
        }
        score, reason = MutualFundStrategies.score_esg(fund_data)
        assert score >= 8  # 5-globe + ESG category

    def test_standard_fund(self):
        """Test standard fund without ESG focus."""
        fund_data = {
            "sustainability_rating": 3,
            "category": "Large Blend",
            "name": "Standard Index Fund",
        }
        score, reason = MutualFundStrategies.score_esg(fund_data)
        assert score == 5 or score == 6  # Neutral score


class TestAnalyzeFund:
    """Tests for the main analyze_fund function."""

    def test_complete_analysis(self):
        """Test complete fund analysis."""
        fund_data = {
            "symbol": "VFIAX",
            "name": "Vanguard 500 Index Fund Admiral Shares",
            "category": "Large Blend",
            "family": "Vanguard",
            "expense_ratio": 0.0004,
            "dividend_yield": 0.015,
            "turnover_rate": 0.03,
            "holdings_count": 500,
            "top_10_holdings_pct": 0.30,
            "net_assets": 400e9,
            "stock_holdings": 0.99,
            "bond_holdings": 0,
            "ytd_return": 0.10,
            "three_year_return": 0.12,
            "five_year_return": 0.14,
            "ten_year_return": 0.13,
            "morningstar_rating": 5,
            "sustainability_rating": 3,
            "beta": 1.0,
            "alpha": 0.5,
            "inception_date": 631152000,
        }
        result = MutualFundStrategies.analyze_fund(fund_data)

        assert "total_score" in result
        assert "average_score" in result
        assert result["total_score"] > 0
        assert result["average_score"] > 0

        # Check all strategies are present
        for strategy_name in STRATEGY_NAMES.keys():
            assert strategy_name in result
            assert "score" in result[strategy_name]
            assert "reason" in result[strategy_name]
            assert 0 <= result[strategy_name]["score"] <= 10

    def test_empty_data(self):
        """Test analysis with empty data."""
        result = MutualFundStrategies.analyze_fund({})
        assert "error" in result or result.get("total_score", 0) == 0

    def test_none_data(self):
        """Test analysis with None data."""
        result = MutualFundStrategies.analyze_fund(None)
        assert "error" in result


class TestStrategyNames:
    """Tests for STRATEGY_NAMES dictionary."""

    def test_all_strategies_named(self):
        """Test that all strategies have display names."""
        expected_strategies = [
            "cost_efficiency",
            "performance_score",
            "manager_quality",
            "risk_adjusted",
            "diversification",
            "tax_efficiency",
            "fund_quality",
            "growth_score",
            "income_score",
            "esg_score",
        ]
        for strategy in expected_strategies:
            assert strategy in STRATEGY_NAMES
            assert isinstance(STRATEGY_NAMES[strategy], str)
            assert len(STRATEGY_NAMES[strategy]) > 0
