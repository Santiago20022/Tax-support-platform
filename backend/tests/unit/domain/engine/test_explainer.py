"""Tests for explanation builder."""

import uuid

import pytest

from app.domain.engine.evaluator import ConditionResult
from app.domain.engine.explainer import ExplanationBuilder
from app.domain.entities.obligation import ObligationTypeEntity
from app.domain.entities.rule import RuleEntity


@pytest.fixture
def explainer():
    return ExplanationBuilder(fiscal_year=2025)


@pytest.fixture
def renta_obligation():
    return ObligationTypeEntity(
        id=uuid.uuid4(),
        code="renta",
        name="Impuesto sobre la Renta y Complementarios",
        category="nacional",
        description="Impuesto anual sobre los ingresos",
        responsible_entity="DIAN",
        legal_base="Art. 592 del Estatuto Tributario; Art. 593 del Estatuto Tributario",
    )


@pytest.fixture
def generic_obligation():
    return ObligationTypeEntity(
        id=uuid.uuid4(),
        code="ica",
        name="Industria y Comercio (ICA)",
        category="territorial",
        description="Impuesto municipal",
        responsible_entity="Secretaría de Hacienda",
        legal_base="Acuerdo 65 de 2002",
    )


class TestExplanationBuilder:
    def test_renta_applies_explanation(self, explainer, renta_obligation):
        conditions = [
            ConditionResult(
                field="ingresos_brutos_cop",
                operator="gte",
                profile_value=180000000,
                threshold_code="renta_pn_ingresos_tope",
                threshold_value=69497400,
                passes=True,
                description="Ingresos >= 1400 UVT",
            )
        ]
        rule = RuleEntity(
            id=uuid.uuid4(),
            rule_set_id=uuid.uuid4(),
            obligation_type_id=renta_obligation.id,
            code="renta_test",
            name="Renta test",
        )

        explanation = explainer.build(renta_obligation, "applies", rule, conditions)
        assert "2025" in explanation
        assert "Renta" in explanation
        assert "obligado" in explanation.lower() or "estaría" in explanation.lower()

    def test_does_not_apply_explanation(self, explainer, renta_obligation):
        explanation = explainer.build(renta_obligation, "does_not_apply", None, [])
        assert "NO" in explanation
        assert "2025" in explanation

    def test_generic_applies(self, explainer, generic_obligation):
        conditions = [
            ConditionResult(
                field="has_comercio_registration",
                operator="is_true",
                profile_value=True,
                threshold_code=None,
                threshold_value=None,
                passes=True,
                description=None,
            )
        ]

        explanation = explainer.build(generic_obligation, "applies", None, conditions)
        assert "ICA" in explanation or "Industria" in explanation

    def test_legal_references(self, explainer, renta_obligation):
        refs = explainer.get_legal_references(renta_obligation, None)
        assert len(refs) == 2
        assert "Art. 592 del Estatuto Tributario" in refs
        assert "Art. 593 del Estatuto Tributario" in refs

    def test_conditional_explanation(self, explainer, generic_obligation):
        explanation = explainer.build(generic_obligation, "conditional", None, [])
        assert "podría" in explanation or "condiciones" in explanation.lower()
