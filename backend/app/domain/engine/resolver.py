"""Threshold resolver - resolves condition values against stored thresholds."""
from __future__ import annotations

from decimal import Decimal

from app.domain.entities.rule import RuleConditionEntity


class ThresholdResolver:
    """Resolves rule condition values against stored thresholds."""

    def __init__(self, thresholds: dict[str, Decimal]) -> None:
        self._thresholds = thresholds

    def resolve(self, condition: RuleConditionEntity) -> tuple[object, object]:
        """
        Resolve condition value(s) based on value_type.

        Returns:
            tuple of (resolved_value, resolved_secondary_value)
        """
        if condition.value_type == "threshold_ref":
            primary = self._resolve_threshold_ref(condition.value)
            secondary = self._resolve_threshold_ref(condition.value_secondary)
            return primary, secondary
        elif condition.value_type == "literal":
            return condition.value, condition.value_secondary
        elif condition.value_type == "uvt_expr":
            return self._resolve_uvt_expr(condition.value), self._resolve_uvt_expr(
                condition.value_secondary
            )
        else:
            return condition.value, condition.value_secondary

    def _resolve_threshold_ref(self, code: str | None) -> Decimal | None:
        if code is None:
            return None
        value = self._thresholds.get(code)
        if value is None:
            raise ValueError(f"Threshold not found: {code}")
        return value

    def _resolve_uvt_expr(self, expr: str | None) -> Decimal | None:
        if expr is None:
            return None
        uvt_value = self._thresholds.get("uvt_value")
        if uvt_value is None:
            raise ValueError("UVT value not found in thresholds")
        return Decimal(str(expr)) * uvt_value

    def get_threshold_value(self, code: str) -> Decimal | None:
        return self._thresholds.get(code)
