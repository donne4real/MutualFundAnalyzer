"""
Tests for ETF Exporter Module
"""

import os
import pytest
from src.exporter import SpreadsheetExporter


class TestSpreadsheetExporter:
    """Tests for the SpreadsheetExporter class."""

    def test_init(self):
        """Test exporter initialization."""
        exporter = SpreadsheetExporter()
        assert exporter is not None
        assert exporter.output_dir == "output"

    def test_init_custom_dir(self):
        """Test exporter with custom output directory."""
        exporter = SpreadsheetExporter(output_dir="test_output")
        assert exporter.output_dir == "test_output"

    def test_get_score_color(self):
        """Test score color assignment."""
        exporter = SpreadsheetExporter()

        # High scores (green)
        assert exporter._get_score_color(8) == exporter.COLORS["high"]
        assert exporter._get_score_color(10) == exporter.COLORS["high"]

        # Medium scores (amber)
        assert exporter._get_score_color(5) == exporter.COLORS["medium"]
        assert exporter._get_score_color(7) == exporter.COLORS["medium"]

        # Low scores (red)
        assert exporter._get_score_color(0) == exporter.COLORS["low"]
        assert exporter._get_score_color(4) == exporter.COLORS["low"]

    def test_get_recommendation(self):
        """Test recommendation assignment."""
        exporter = SpreadsheetExporter()

        assert exporter._get_recommendation(75) == "Strong Buy"
        assert exporter._get_recommendation(70) == "Strong Buy"
        assert exporter._get_recommendation(60) == "Buy"
        assert exporter._get_recommendation(50) == "Buy"
        assert exporter._get_recommendation(40) == "Hold"
        assert exporter._get_recommendation(30) == "Hold"
        assert exporter._get_recommendation(20) == "Avoid"
        assert exporter._get_recommendation(0) == "Avoid"

    def test_export_to_excel(self, tmp_path):
        """Test Excel export."""
        exporter = SpreadsheetExporter(output_dir=str(tmp_path))

        etfs_data = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "category": "Large Blend",
                "family": "SPDR",
                "price": 450.00,
                "expense_ratio": 0.0009,
            }
        ]

        strategies_data = [
            {
                "total_score": 75,
                "average_score": 7.5,
                "value_score": {"score": 8, "reason": "Low cost"},
                "momentum": {"score": 7, "reason": "Good momentum"},
                "quality_score": {"score": 8, "reason": "Quality fund"},
                "growth_score": {"score": 7, "reason": "Good growth"},
                "dividend_score": {"score": 6, "reason": "Moderate yield"},
                "risk_adjusted": {"score": 8, "reason": "Low risk"},
                "diversification": {"score": 9, "reason": "Well diversified"},
                "cost_efficiency": {"score": 9, "reason": "Low cost"},
                "liquidity_score": {"score": 10, "reason": "High liquidity"},
                "esg_score": {"score": 5, "reason": "Standard"},
            }
        ]

        filepath = exporter.export_to_excel(etfs_data, strategies_data)

        assert os.path.exists(filepath)
        assert filepath.endswith(".xlsx")

    def test_export_to_csv(self, tmp_path):
        """Test CSV export."""
        exporter = SpreadsheetExporter(output_dir=str(tmp_path))

        etfs_data = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "category": "Large Blend",
                "price": 450.00,
            }
        ]

        strategies_data = [
            {
                "total_score": 75,
                "average_score": 7.5,
                "value_score": {"score": 8, "reason": "Low cost"},
                "momentum": {"score": 7, "reason": "Good momentum"},
                "quality_score": {"score": 8, "reason": "Quality fund"},
                "growth_score": {"score": 7, "reason": "Good growth"},
                "dividend_score": {"score": 6, "reason": "Moderate yield"},
                "risk_adjusted": {"score": 8, "reason": "Low risk"},
                "diversification": {"score": 9, "reason": "Well diversified"},
                "cost_efficiency": {"score": 9, "reason": "Low cost"},
                "liquidity_score": {"score": 10, "reason": "High liquidity"},
                "esg_score": {"score": 5, "reason": "Standard"},
            }
        ]

        filepath = exporter.export_to_csv(etfs_data, strategies_data)

        assert os.path.exists(filepath)
        assert filepath.endswith(".csv")

    def test_empty_data_export(self, tmp_path):
        """Test export with empty data."""
        exporter = SpreadsheetExporter(output_dir=str(tmp_path))

        # Excel export with empty data
        filepath = exporter.export_to_excel([], [])
        assert os.path.exists(filepath)

        # CSV export with empty data
        filepath = exporter.export_to_csv([], [])
        assert os.path.exists(filepath)
