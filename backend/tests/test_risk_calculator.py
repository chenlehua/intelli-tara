"""
Tests for risk calculator service.
"""
import pytest
import sys
sys.path.insert(0, '.')

from app.services.risk_calculator import RiskCalculator


class TestRiskCalculator:
    """Tests for RiskCalculator class."""

    def test_calculate_feasibility_high(self):
        """Test attack feasibility calculation - high feasibility scenario."""
        result, label = RiskCalculator.calculate_feasibility(
            attack_vector="Network",
            attack_complexity="Low",
            privileges_required="None",
            user_interaction="None",
        )
        assert result == 3  # High feasibility (sum = 3+1+2+1 = 7)
        assert label == "High"

    def test_calculate_feasibility_very_low(self):
        """Test attack feasibility calculation - very low feasibility."""
        result, label = RiskCalculator.calculate_feasibility(
            attack_vector="Physical",
            attack_complexity="High",
            privileges_required="High",
            user_interaction="Required",
        )
        assert result == 0  # Very Low (sum = 0+0+0+0 = 0)
        assert label == "Very Low"

    def test_calculate_impact_severe(self):
        """Test impact level calculation - severe impact (using S3)."""
        result, label = RiskCalculator.calculate_impact(
            safety="S3",
            financial="F2",
            operational="O1",
            privacy="P2",
        )
        assert result == 3  # Severe (max of all values)
        assert label == "Severe"

    def test_calculate_impact_negligible(self):
        """Test impact level calculation - negligible impact."""
        result, label = RiskCalculator.calculate_impact(
            safety="S0",
            financial="F0",
            operational="O0",
            privacy="P0",
        )
        assert result == 0  # Negligible
        assert label == "Negligible"

    def test_calculate_impact_none_values(self):
        """Test impact level with no values."""
        result, label = RiskCalculator.calculate_impact(
            safety=None,
            financial=None,
            operational=None,
            privacy=None,
        )
        assert result is None
        assert label is None

    def test_calculate_risk_level_matrix(self):
        """Test risk level calculation based on matrix."""
        # High feasibility (3) + Severe impact (3) = Risk level 5 (严重)
        result, label = RiskCalculator.calculate_risk_level(3, 3)
        assert result == 5
        assert label == "严重"

        # Very Low feasibility (0) + Negligible impact (0) = Risk level 1 (可接受)
        result, label = RiskCalculator.calculate_risk_level(0, 0)
        assert result == 1
        assert label == "可接受"

        # Medium feasibility (2) + Moderate impact (1) = Risk level 2 (低)
        result, label = RiskCalculator.calculate_risk_level(2, 1)
        assert result == 2
        assert label == "低"

    def test_calculate_risk_level_none_input(self):
        """Test risk level with None inputs."""
        result, label = RiskCalculator.calculate_risk_level(None, 3)
        assert result is None
        assert label is None

        result, label = RiskCalculator.calculate_risk_level(3, None)
        assert result is None
        assert label is None

    def test_suggest_treatment(self):
        """Test treatment suggestion based on risk level."""
        assert RiskCalculator.suggest_treatment(1) == "Accept"
        assert RiskCalculator.suggest_treatment(2) == "Accept"
        assert RiskCalculator.suggest_treatment(3) == "Reduce"
        assert RiskCalculator.suggest_treatment(4) == "Reduce"
        assert RiskCalculator.suggest_treatment(5) == "Avoid"
        assert RiskCalculator.suggest_treatment(None) == "Accept"

    def test_full_risk_assessment(self):
        """Test complete risk assessment workflow."""
        # Calculate feasibility
        feasibility, feas_label = RiskCalculator.calculate_feasibility(
            attack_vector="Network",
            attack_complexity="Low",
            privileges_required="Low",
            user_interaction="None",
        )
        assert feasibility is not None
        assert feas_label is not None
        
        # Calculate impact
        impact, impact_label = RiskCalculator.calculate_impact(
            safety="S0",
            financial="F2",
            operational="O1",
            privacy="P2",
        )
        assert impact is not None
        assert impact_label is not None
        
        # Calculate final risk
        risk, risk_label = RiskCalculator.calculate_risk_level(feasibility, impact)
        
        assert 1 <= risk <= 5
        assert risk_label in ["可接受", "低", "中", "高", "严重"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
