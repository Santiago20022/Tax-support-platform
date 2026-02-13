"""Rule evaluator - evaluates rules against a tax profile."""
from __future__ import annotations

from dataclasses import dataclass

from app.domain.engine.operators import apply_operator
from app.domain.engine.resolver import ThresholdResolver
from app.domain.entities.rule import RuleConditionEntity, RuleEntity
from app.domain.entities.tax_profile import TaxProfileEntity


@dataclass
class ConditionResult:
    field: str
    operator: str
    profile_value: object
    threshold_code: str | None
    threshold_value: object
    passes: bool
    description: str | None


@dataclass
class RuleEvaluation:
    rule: RuleEntity
    passes: bool
    condition_results: list[ConditionResult]


class RuleEvaluator:
    """Evaluates rules against a tax profile using threshold resolution."""

    def __init__(self, resolver: ThresholdResolver) -> None:
        self._resolver = resolver

    def evaluate_rule(self, rule: RuleEntity, profile: TaxProfileEntity) -> RuleEvaluation:
        condition_results: list[ConditionResult] = []

        for condition in rule.conditions:
            result = self._evaluate_condition(condition, profile)
            condition_results.append(result)

        if rule.logic_operator.upper() == "AND":
            passes = all(cr.passes for cr in condition_results)
        else:  # OR
            passes = any(cr.passes for cr in condition_results)

        return RuleEvaluation(
            rule=rule,
            passes=passes,
            condition_results=condition_results,
        )

    def _evaluate_condition(
        self, condition: RuleConditionEntity, profile: TaxProfileEntity
    ) -> ConditionResult:
        profile_value = profile.get_field_value(condition.field)
        resolved_value, resolved_secondary = self._resolver.resolve(condition)

        threshold_code = (
            condition.value if condition.value_type == "threshold_ref" else None
        )

        passes = apply_operator(
            condition.operator,
            profile_value,
            resolved_value,
            resolved_secondary,
        )

        return ConditionResult(
            field=condition.field,
            operator=condition.operator,
            profile_value=self._serialize_value(profile_value),
            threshold_code=threshold_code,
            threshold_value=self._serialize_value(resolved_value),
            passes=passes,
            description=condition.description,
        )

    @staticmethod
    def _serialize_value(value: object) -> object:
        from decimal import Decimal

        if isinstance(value, Decimal):
            return float(value)
        return value
