"""Tests for the rule evaluator."""

import uuid
from decimal import Decimal

import pytest

from app.domain.engine.evaluator import RuleEvaluator
from app.domain.engine.resolver import ThresholdResolver
from app.domain.entities.rule import RuleConditionEntity, RuleEntity
from app.domain.entities.tax_profile import TaxProfileEntity


@pytest.fixture
def thresholds():
    return {
        "renta_pn_ingresos_tope": Decimal("69497400"),
        "renta_pn_patrimonio_tope": Decimal("223384500"),
        "iva_responsable_tope": Decimal("173743500"),
    }


@pytest.fixture
def resolver(thresholds):
    return ThresholdResolver(thresholds)


@pytest.fixture
def evaluator(resolver):
    return RuleEvaluator(resolver)


@pytest.fixture
def profile_high_income():
    return TaxProfileEntity(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        fiscal_year_id=uuid.uuid4(),
        persona_type="natural_comerciante",
        regime="ordinario",
        is_iva_responsable=False,
        ingresos_brutos_cop=Decimal("180000000"),
        patrimonio_bruto_cop=Decimal("200000000"),
        has_employees=True,
        employee_count=3,
        city="Bogotá",
        has_comercio_registration=True,
    )


@pytest.fixture
def profile_low_income():
    return TaxProfileEntity(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        fiscal_year_id=uuid.uuid4(),
        persona_type="natural",
        regime="ordinario",
        is_iva_responsable=False,
        ingresos_brutos_cop=Decimal("30000000"),
        patrimonio_bruto_cop=Decimal("50000000"),
        has_employees=False,
        employee_count=0,
    )


class TestRuleEvaluator:
    def test_and_rule_all_pass(self, evaluator, profile_high_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_and",
            name="Test AND rule",
            logic_operator="AND",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="regime",
                    operator="eq",
                    value_type="literal",
                    value="ordinario",
                ),
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="ingresos_brutos_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="iva_responsable_tope",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_high_income)
        assert result.passes is True
        assert all(cr.passes for cr in result.condition_results)

    def test_and_rule_one_fails(self, evaluator, profile_low_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_and_fail",
            name="Test AND rule fail",
            logic_operator="AND",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="regime",
                    operator="eq",
                    value_type="literal",
                    value="ordinario",
                ),
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="ingresos_brutos_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="iva_responsable_tope",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_low_income)
        assert result.passes is False

    def test_or_rule_one_passes(self, evaluator, profile_high_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_or",
            name="Test OR rule",
            logic_operator="OR",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="ingresos_brutos_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="renta_pn_ingresos_tope",
                ),
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="patrimonio_bruto_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="renta_pn_patrimonio_tope",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_high_income)
        assert result.passes is True

    def test_or_rule_none_pass(self, evaluator, profile_low_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_or_fail",
            name="Test OR rule fail",
            logic_operator="OR",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="ingresos_brutos_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="renta_pn_ingresos_tope",
                ),
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="patrimonio_bruto_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="renta_pn_patrimonio_tope",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_low_income)
        assert result.passes is False

    def test_boolean_condition(self, evaluator, profile_high_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_bool",
            name="Test boolean",
            logic_operator="AND",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="has_employees",
                    operator="is_true",
                    value_type="literal",
                    value="true",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_high_income)
        assert result.passes is True

    def test_condition_result_has_values(self, evaluator, profile_high_income):
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=uuid.uuid4(),
            code="test_values",
            name="Test values",
            logic_operator="AND",
            conditions=[
                RuleConditionEntity(
                    id=uuid.uuid4(),
                    rule_id=uuid.uuid4(),
                    field="ingresos_brutos_cop",
                    operator="gte",
                    value_type="threshold_ref",
                    value="renta_pn_ingresos_tope",
                    description="Ingresos >= 1400 UVT",
                ),
            ],
        )

        result = evaluator.evaluate_rule(rule, profile_high_income)
        cr = result.condition_results[0]
        assert cr.field == "ingresos_brutos_cop"
        assert cr.operator == "gte"
        assert cr.profile_value == 180000000.0
        assert cr.threshold_code == "renta_pn_ingresos_tope"
        assert cr.threshold_value == 69497400.0
        assert cr.passes is True
