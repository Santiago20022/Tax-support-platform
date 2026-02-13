"""Explanation builder - generates clear explanations for evaluation results."""
from __future__ import annotations

from decimal import Decimal

from app.domain.engine.evaluator import ConditionResult
from app.domain.entities.obligation import ObligationTypeEntity
from app.domain.entities.rule import RuleEntity
from app.domain.value_objects.evaluation_result import ObligationResult


EXPLANATION_TEMPLATES: dict[str, str] = {
    "renta_applies": (
        "Usted estaría obligado a presentar declaración de Renta para el año gravable {fiscal_year} "
        "porque {reason}. Base legal: {legal_reference}."
    ),
    "renta_does_not_apply": (
        "Con base en la información suministrada, usted NO estaría obligado a presentar "
        "declaración de Renta para {fiscal_year}, ya que no supera ninguno de los topes "
        "establecidos (ingresos, patrimonio, consignaciones, compras)."
    ),
    "iva_applies": (
        "Usted estaría en la condición de responsable de IVA porque {reason}. "
        "Base legal: {legal_reference}."
    ),
    "generic_applies": (
        "Usted estaría obligado a cumplir con {obligation_name} porque {reason}. "
        "{legal_note}"
    ),
    "generic_does_not_apply": (
        "Con base en la información suministrada, la obligación de {obligation_name} "
        "no le aplicaría para {fiscal_year}."
    ),
    "generic_conditional": (
        "La obligación de {obligation_name} podría aplicarle bajo ciertas condiciones "
        "adicionales. Consulte con su contador para confirmar. {legal_note}"
    ),
    "generic_needs_more_info": (
        "Se requiere información adicional para determinar si la obligación de "
        "{obligation_name} le aplica. Por favor complete los datos faltantes en su perfil."
    ),
}


def _format_cop(value: object) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, (int, float, Decimal)):
        return f"${value:,.0f} COP"
    return str(value)


def _build_reason_from_conditions(conditions: list[ConditionResult]) -> str:
    passing = [c for c in conditions if c.passes]
    if not passing:
        return "se cumplen las condiciones establecidas"

    reasons = []
    for c in passing:
        if c.operator in ("gte", "gt"):
            reasons.append(
                f"su campo {c.field.replace('_', ' ')} ({_format_cop(c.profile_value)}) "
                f"supera el tope de {_format_cop(c.threshold_value)}"
            )
        elif c.operator in ("eq",):
            reasons.append(f"su {c.field.replace('_', ' ')} es {c.profile_value}")
        elif c.operator in ("is_true",):
            reasons.append(f"cumple con {c.field.replace('_', ' ')}")
        elif c.operator in ("is_false",):
            reasons.append(f"no cumple con {c.field.replace('_', ' ')}")
        elif c.description:
            reasons.append(c.description)
        else:
            reasons.append(f"cumple la condición sobre {c.field.replace('_', ' ')}")

    return "; ".join(reasons)


class ExplanationBuilder:
    """Builds user-friendly explanations for evaluation results."""

    def __init__(self, fiscal_year: int) -> None:
        self._fiscal_year = fiscal_year

    def build(
        self,
        obligation: ObligationTypeEntity,
        result: str,
        triggered_rule: RuleEntity | None,
        conditions: list[ConditionResult],
    ) -> str:
        reason = _build_reason_from_conditions(conditions)
        legal_note = f"Base legal: {obligation.legal_base}." if obligation.legal_base else ""
        legal_reference = obligation.legal_base or ""

        template_key = f"{obligation.code}_{result}"
        if template_key not in EXPLANATION_TEMPLATES:
            template_key = f"generic_{result}"

        template = EXPLANATION_TEMPLATES.get(template_key, EXPLANATION_TEMPLATES["generic_applies"])

        return template.format(
            fiscal_year=self._fiscal_year,
            obligation_name=obligation.name,
            reason=reason,
            legal_reference=legal_reference,
            legal_note=legal_note,
        )

    def get_legal_references(
        self, obligation: ObligationTypeEntity, triggered_rule: RuleEntity | None
    ) -> list[str]:
        refs = []
        if obligation.legal_base:
            refs.extend(
                ref.strip()
                for ref in obligation.legal_base.split(";")
                if ref.strip()
            )
        return refs
