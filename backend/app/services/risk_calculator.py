"""Risk calculation service based on ISO 21434."""

from typing import Optional, Tuple

from app.models.threat import ThreatScenario


class RiskCalculator:
    """Risk calculation utilities for TARA analysis."""

    # Attack vector mapping
    ATTACK_VECTOR_VALUES = {
        "Physical": 0,
        "Local": 1,
        "Adjacent": 2,
        "Network": 3,
    }

    # Attack complexity mapping
    ATTACK_COMPLEXITY_VALUES = {
        "High": 0,
        "Low": 1,
    }

    # Privileges required mapping
    PRIVILEGES_REQUIRED_VALUES = {
        "High": 0,
        "Low": 1,
        "None": 2,
    }

    # User interaction mapping
    USER_INTERACTION_VALUES = {
        "Required": 0,
        "None": 1,
    }

    # Impact level mapping
    IMPACT_VALUES = {
        "S0": 0, "S1": 1, "S2": 2, "S3": 3,
        "F0": 0, "F1": 1, "F2": 2, "F3": 3,
        "O0": 0, "O1": 1, "O2": 2, "O3": 3,
        "P0": 0, "P1": 1, "P2": 2, "P3": 3,
    }

    # Feasibility calculation matrix
    # Sum of all parameters determines feasibility level
    # 0-2: Very Low, 3-4: Low, 5-6: Medium, 7-8: High
    FEASIBILITY_THRESHOLDS = [
        (2, "Very Low", 0),
        (4, "Low", 1),
        (6, "Medium", 2),
        (8, "High", 3),
    ]

    # Impact level labels
    IMPACT_LABELS = ["Negligible", "Moderate", "Major", "Severe"]

    # Risk matrix (feasibility x impact)
    # 4x4 matrix where rows are feasibility (0=Very Low to 3=High)
    # and columns are impact (0=Negligible to 3=Severe)
    RISK_MATRIX = [
        [1, 1, 1, 2],  # Very Low feasibility
        [1, 1, 2, 3],  # Low feasibility
        [1, 2, 3, 4],  # Medium feasibility
        [2, 3, 4, 5],  # High feasibility
    ]

    # Risk level labels
    RISK_LABELS = {
        1: "可接受",
        2: "低",
        3: "中",
        4: "高",
        5: "严重",
    }

    @classmethod
    def calculate_feasibility(
        cls,
        attack_vector: Optional[str],
        attack_complexity: Optional[str],
        privileges_required: Optional[str],
        user_interaction: Optional[str],
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Calculate attack feasibility based on CVSS-like parameters.

        Returns:
            Tuple of (feasibility_value, feasibility_label)
        """
        if not all([attack_vector, attack_complexity, privileges_required, user_interaction]):
            return None, None

        # Calculate sum of parameter values
        total = (
            cls.ATTACK_VECTOR_VALUES.get(attack_vector, 0) +
            cls.ATTACK_COMPLEXITY_VALUES.get(attack_complexity, 0) +
            cls.PRIVILEGES_REQUIRED_VALUES.get(privileges_required, 0) +
            cls.USER_INTERACTION_VALUES.get(user_interaction, 0)
        )

        # Determine feasibility level
        for threshold, label, value in cls.FEASIBILITY_THRESHOLDS:
            if total <= threshold:
                return value, label

        return 3, "High"

    @classmethod
    def calculate_impact(
        cls,
        safety: Optional[str],
        financial: Optional[str],
        operational: Optional[str],
        privacy: Optional[str],
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Calculate impact level as the maximum of all impact dimensions.

        Returns:
            Tuple of (impact_value, impact_label)
        """
        values = []

        if safety:
            values.append(cls.IMPACT_VALUES.get(safety, 0))
        if financial:
            values.append(cls.IMPACT_VALUES.get(financial, 0))
        if operational:
            values.append(cls.IMPACT_VALUES.get(operational, 0))
        if privacy:
            values.append(cls.IMPACT_VALUES.get(privacy, 0))

        if not values:
            return None, None

        max_value = max(values)
        return max_value, cls.IMPACT_LABELS[max_value]

    @classmethod
    def calculate_risk_level(
        cls,
        feasibility_value: Optional[int],
        impact_value: Optional[int],
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Calculate risk level from feasibility and impact using risk matrix.

        Returns:
            Tuple of (risk_level, risk_label)
        """
        if feasibility_value is None or impact_value is None:
            return None, None

        # Ensure values are within bounds
        feas_idx = min(max(feasibility_value, 0), 3)
        impact_idx = min(max(impact_value, 0), 3)

        risk_level = cls.RISK_MATRIX[feas_idx][impact_idx]
        risk_label = cls.RISK_LABELS.get(risk_level, "未知")

        return risk_level, risk_label

    @classmethod
    def calculate_and_update_threat(cls, threat: ThreatScenario) -> ThreatScenario:
        """
        Calculate all risk metrics and update the threat scenario.

        Args:
            threat: ThreatScenario object to update

        Returns:
            Updated ThreatScenario object
        """
        # Calculate feasibility
        feas_value, feas_label = cls.calculate_feasibility(
            threat.attack_vector,
            threat.attack_complexity,
            threat.privileges_required,
            threat.user_interaction,
        )
        threat.attack_feasibility_value = feas_value
        threat.attack_feasibility = feas_label

        # Calculate impact
        impact_value, impact_label = cls.calculate_impact(
            threat.impact_safety,
            threat.impact_financial,
            threat.impact_operational,
            threat.impact_privacy,
        )
        threat.impact_level_value = impact_value
        threat.impact_level = impact_label

        # Calculate risk level
        risk_level, risk_label = cls.calculate_risk_level(feas_value, impact_value)
        threat.risk_level = risk_level
        threat.risk_level_label = risk_label

        return threat

    @classmethod
    def suggest_treatment(cls, risk_level: Optional[int]) -> str:
        """
        Suggest risk treatment based on risk level.

        Args:
            risk_level: Risk level (1-5)

        Returns:
            Suggested treatment decision
        """
        if not risk_level:
            return "Accept"

        if risk_level <= 1:
            return "Accept"
        elif risk_level <= 2:
            return "Accept"  # Consider reducing
        elif risk_level <= 3:
            return "Reduce"
        elif risk_level <= 4:
            return "Reduce"  # Must reduce
        else:
            return "Avoid"  # Critical - must avoid or strongly reduce
