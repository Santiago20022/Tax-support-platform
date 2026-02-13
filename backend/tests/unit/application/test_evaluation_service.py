"""Tests for the rules engine end-to-end evaluation."""

import uuid
from decimal import Decimal

import pytest

from app.domain.engine.engine import RulesEngine
from app.domain.entities.obligation import ObligationTypeEntity
from app.domain.entities.rule import RuleConditionEntity, RuleEntity, RuleSetEntity
from app.domain.entities.tax_profile import TaxProfileEntity


@pytest.fixture
def thresholds_2025():
    uvt = Decimal("49641")
    return {
        "renta_pn_ingresos_tope": Decimal("1400") * uvt,
        "renta_pn_patrimonio_tope": Decimal("4500") * uvt,
        "renta_pn_consignaciones_tope": Decimal("1400") * uvt,
        "renta_pn_compras_tope": Decimal("1400") * uvt,
        "iva_responsable_tope": Decimal("3500") * uvt,
        "retefuente_agente_tope": Decimal("30000") * uvt,
        "exogena_tope": Decimal("2016") * uvt,
    }


@pytest.fixture
def obligations():
    return [
        ObligationTypeEntity(
            id=uuid.UUID("10000000-0000-0000-0000-000000000001"),
            code="renta",
            name="Impuesto sobre la Renta",
            category="nacional",
            description="Renta",
            responsible_entity="DIAN",
            legal_base="Art. 592 del Estatuto Tributario; Art. 593 del Estatuto Tributario",
        ),
        ObligationTypeEntity(
            id=uuid.UUID("10000000-0000-0000-0000-000000000002"),
            code="iva",
            name="IVA",
            category="nacional",
            description="IVA",
            responsible_entity="DIAN",
            legal_base="Art. 437 del Estatuto Tributario",
        ),
        ObligationTypeEntity(
            id=uuid.UUID("10000000-0000-0000-0000-000000000003"),
            code="nomina_seguridad_social",
            name="Nómina y Seguridad Social",
            category="laboral",
            description="PILA",
            responsible_entity="Operadores PILA",
            legal_base="Ley 100 de 1993",
        ),
    ]


@pytest.fixture
def rule_set(obligations):
    rs_id = uuid.uuid4()
    return RuleSetEntity(
        id=rs_id,
        fiscal_year_id=uuid.uuid4(),
        version=1,
        status="active",
        rules=[
            RuleEntity(
                id=uuid.uuid4(),
                rule_set_id=rs_id,
                obligation_type_id=obligations[0].id,
                code="renta_pn_ingresos",
                name="Renta por ingresos",
                logic_operator="OR",
                priority=1,
                result_if_true="applies",
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
            ),
            RuleEntity(
                id=uuid.uuid4(),
                rule_set_id=rs_id,
                obligation_type_id=obligations[1].id,
                code="iva_responsable",
                name="IVA responsable",
                logic_operator="AND",
                priority=1,
                result_if_true="applies",
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
            ),
            RuleEntity(
                id=uuid.uuid4(),
                rule_set_id=rs_id,
                obligation_type_id=obligations[2].id,
                code="nomina_empleados",
                name="Nómina empleados",
                logic_operator="AND",
                priority=1,
                result_if_true="applies",
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
            ),
        ],
    )


@pytest.fixture
def high_income_profile():
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
def low_income_profile():
    return TaxProfileEntity(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        fiscal_year_id=uuid.uuid4(),
        persona_type="natural",
        regime="simple",
        is_iva_responsable=False,
        ingresos_brutos_cop=Decimal("30000000"),
        patrimonio_bruto_cop=Decimal("50000000"),
        has_employees=False,
        employee_count=0,
    )


class TestRulesEngineEvaluation:
    def test_high_income_all_apply(
        self, thresholds_2025, high_income_profile, rule_set, obligations
    ):
        engine = RulesEngine(thresholds=thresholds_2025, fiscal_year=2025)
        rules_by_ob = {}
        for rule in rule_set.rules:
            rules_by_ob.setdefault(rule.obligation_type_id, []).append(rule)

        results = engine.evaluate(high_income_profile, rule_set, obligations, rules_by_ob)

        assert len(results) == 3
        renta_result = next(r for r in results if r.obligation_code == "renta")
        iva_result = next(r for r in results if r.obligation_code == "iva")
        nomina_result = next(r for r in results if r.obligation_code == "nomina_seguridad_social")

        assert renta_result.result == "applies"
        assert iva_result.result == "applies"
        assert nomina_result.result == "applies"

    def test_low_income_none_apply(
        self, thresholds_2025, low_income_profile, rule_set, obligations
    ):
        engine = RulesEngine(thresholds=thresholds_2025, fiscal_year=2025)
        rules_by_ob = {}
        for rule in rule_set.rules:
            rules_by_ob.setdefault(rule.obligation_type_id, []).append(rule)

        results = engine.evaluate(low_income_profile, rule_set, obligations, rules_by_ob)

        assert len(results) == 3
        for result in results:
            assert result.result == "does_not_apply"

    def test_results_have_explanations(
        self, thresholds_2025, high_income_profile, rule_set, obligations
    ):
        engine = RulesEngine(thresholds=thresholds_2025, fiscal_year=2025)
        rules_by_ob = {}
        for rule in rule_set.rules:
            rules_by_ob.setdefault(rule.obligation_type_id, []).append(rule)

        results = engine.evaluate(high_income_profile, rule_set, obligations, rules_by_ob)

        for result in results:
            assert result.explanation_es != ""
            assert isinstance(result.explanation_es, str)

    def test_results_have_conditions_evaluated(
        self, thresholds_2025, high_income_profile, rule_set, obligations
    ):
        engine = RulesEngine(thresholds=thresholds_2025, fiscal_year=2025)
        rules_by_ob = {}
        for rule in rule_set.rules:
            rules_by_ob.setdefault(rule.obligation_type_id, []).append(rule)

        results = engine.evaluate(high_income_profile, rule_set, obligations, rules_by_ob)

        renta_result = next(r for r in results if r.obligation_code == "renta")
        assert len(renta_result.conditions_evaluated) > 0
        first_condition = renta_result.conditions_evaluated[0]
        assert "field" in first_condition
        assert "passes" in first_condition

    def test_different_thresholds_different_results(self, obligations, rule_set):
        """Same profile, different thresholds → different results."""
        profile = TaxProfileEntity(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            tenant_id=uuid.uuid4(),
            fiscal_year_id=uuid.uuid4(),
            persona_type="natural",
            regime="ordinario",
            is_iva_responsable=False,
            ingresos_brutos_cop=Decimal("100000000"),  # 100M COP
            has_employees=False,
        )

        # With low thresholds (should trigger)
        low_thresholds = {
            "renta_pn_ingresos_tope": Decimal("50000000"),
            "renta_pn_patrimonio_tope": Decimal("200000000"),
            "iva_responsable_tope": Decimal("50000000"),
            "retefuente_agente_tope": Decimal("500000000"),
            "exogena_tope": Decimal("50000000"),
        }
        engine_low = RulesEngine(thresholds=low_thresholds, fiscal_year=2025)
        rules_by_ob = {}
        for rule in rule_set.rules:
            rules_by_ob.setdefault(rule.obligation_type_id, []).append(rule)

        results_low = engine_low.evaluate(profile, rule_set, obligations, rules_by_ob)
        renta_low = next(r for r in results_low if r.obligation_code == "renta")
        assert renta_low.result == "applies"

        # With high thresholds (should NOT trigger)
        high_thresholds = {
            "renta_pn_ingresos_tope": Decimal("200000000"),
            "renta_pn_patrimonio_tope": Decimal("500000000"),
            "iva_responsable_tope": Decimal("200000000"),
            "retefuente_agente_tope": Decimal("1000000000"),
            "exogena_tope": Decimal("200000000"),
        }
        engine_high = RulesEngine(thresholds=high_thresholds, fiscal_year=2025)
        results_high = engine_high.evaluate(profile, rule_set, obligations, rules_by_ob)
        renta_high = next(r for r in results_high if r.obligation_code == "renta")
        assert renta_high.result == "does_not_apply"
