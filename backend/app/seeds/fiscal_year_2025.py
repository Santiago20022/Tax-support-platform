"""Seed data for fiscal year 2025."""

from decimal import Decimal

FISCAL_YEAR_2025 = {
    "year": 2025,
    "status": "active",
    "uvt_value": Decimal("49641"),
    "notes": "Año gravable 2025. UVT fijado por Resolución DIAN.",
}

PERIODICITIES_2025 = [
    {"obligation_code": "renta", "frequency": "anual", "description": "Declaración anual de renta"},
    {"obligation_code": "iva", "frequency": "bimestral", "description": "Declaración bimestral de IVA"},
    {"obligation_code": "ica", "frequency": "bimestral", "description": "Declaración bimestral de ICA (Bogotá)"},
    {"obligation_code": "retefuente", "frequency": "mensual", "description": "Declaración mensual de retención en la fuente"},
    {"obligation_code": "nomina_seguridad_social", "frequency": "mensual", "description": "Pago mensual PILA"},
    {"obligation_code": "exogena", "frequency": "anual", "description": "Reporte anual de información exógena"},
]
