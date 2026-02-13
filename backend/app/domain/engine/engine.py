"""Core rules engine - orchestrates the evaluation of tax profiles against rules."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from app.domain.engine.evaluator import RuleEvaluator
from app.domain.engine.explainer import ExplanationBuilder
from app.domain.engine.resolver import ThresholdResolver
from app.domain.entities.evaluation import EvaluationResultEntity
from app.domain.entities.obligation import ObligationTypeEntity
from app.domain.entities.rule import RuleEntity, RuleSetEntity
from app.domain.entities.tax_profile import TaxProfileEntity
from app.domain.value_objects.evaluation_result import ObligationResult


class RulesEngine:
    """
    Core rules engine that evaluates a tax profile against a rule set
    to determine which tax obligations apply.
    """

    def __init__(
        self,
        thresholds: dict[str, Decimal],
        fiscal_year: int,
    ) -> None:
        self._resolver = ThresholdResolver(thresholds)
        self._evaluator = RuleEvaluator(self._resolver)
        self._explainer = ExplanationBuilder(fiscal_year)

    def evaluate(
        self,
        profile: TaxProfileEntity,
        rule_set: RuleSetEntity,
        obligations: list[ObligationTypeEntity],
        rules_by_obligation: dict[UUID, list[RuleEntity]],
    ) -> list[EvaluationResultEntity]:
        results: list[EvaluationResultEntity] = []

        for obligation in obligations:
            rules = rules_by_obligation.get(obligation.id, [])
            rules_sorted = sorted(rules, key=lambda r: r.priority)

            result = self._evaluate_obligation(profile, obligation, rules_sorted)
            results.append(result)

        return results

    def _evaluate_obligation(
        self,
        profile: TaxProfileEntity,
        obligation: ObligationTypeEntity,
        rules: list[RuleEntity],
    ) -> EvaluationResultEntity:
        obligation_result = ObligationResult.DOES_NOT_APPLY
        triggered_rule: RuleEntity | None = None
        all_conditions: list[dict] = []

        for rule in rules:
            if not rule.is_active:
                continue

            evaluation = self._evaluator.evaluate_rule(rule, profile)
            conditions_log = [
                {
                    "field": cr.field,
                    "operator": cr.operator,
                    "profile_value": cr.profile_value,
                    "threshold_code": cr.threshold_code,
                    "threshold_value": cr.threshold_value,
                    "passes": cr.passes,
                    "description": cr.description,
                }
                for cr in evaluation.condition_results
            ]
            all_conditions.extend(conditions_log)

            if evaluation.passes:
                obligation_result = ObligationResult(rule.result_if_true)
                triggered_rule = rule
                break

        explanation = self._explainer.build(
            obligation,
            obligation_result.value,
            triggered_rule,
            self._evaluator.evaluate_rule(triggered_rule, profile).condition_results
            if triggered_rule
            else [],
        )

        legal_refs = self._explainer.get_legal_references(obligation, triggered_rule)

        return EvaluationResultEntity(
            obligation_type_id=obligation.id,
            obligation_code=obligation.code,
            obligation_name=obligation.name,
            result=obligation_result.value,
            periodicity=None,
            responsible_entity=obligation.responsible_entity,
            triggered_rule_id=triggered_rule.id if triggered_rule else None,
            conditions_evaluated=all_conditions,
            explanation_es=explanation,
            legal_references=legal_refs,
        )
