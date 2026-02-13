"""Seed data for thresholds fiscal year 2025."""

from decimal import Decimal

UVT_2025 = Decimal("49641")

THRESHOLDS_2025 = [
    {
        "code": "renta_pn_ingresos_tope",
        "label": "Tope ingresos brutos para declarar Renta (PN)",
        "value_uvt": Decimal("1400"),
        "value_cop": Decimal("1400") * UVT_2025,
        "description": "1.400 UVT — Tope de ingresos brutos para obligación de declarar renta persona natural",
        "legal_reference": "Art. 592 y 593 del Estatuto Tributario",
    },
    {
        "code": "renta_pn_patrimonio_tope",
        "label": "Tope patrimonio bruto para declarar Renta (PN)",
        "value_uvt": Decimal("4500"),
        "value_cop": Decimal("4500") * UVT_2025,
        "description": "4.500 UVT — Tope de patrimonio bruto para obligación de declarar renta persona natural",
        "legal_reference": "Art. 592 y 593 del Estatuto Tributario",
    },
    {
        "code": "renta_pn_consignaciones_tope",
        "label": "Tope consignaciones bancarias para declarar Renta (PN)",
        "value_uvt": Decimal("1400"),
        "value_cop": Decimal("1400") * UVT_2025,
        "description": "1.400 UVT — Tope de consignaciones bancarias acumuladas",
        "legal_reference": "Art. 592 y 593 del Estatuto Tributario",
    },
    {
        "code": "renta_pn_compras_tope",
        "label": "Tope compras y consumos tarjeta para declarar Renta (PN)",
        "value_uvt": Decimal("1400"),
        "value_cop": Decimal("1400") * UVT_2025,
        "description": "1.400 UVT — Tope de compras y consumos con tarjeta",
        "legal_reference": "Art. 592 y 593 del Estatuto Tributario",
    },
    {
        "code": "iva_responsable_tope",
        "label": "Tope ingresos para ser responsable de IVA",
        "value_uvt": Decimal("3500"),
        "value_cop": Decimal("3500") * UVT_2025,
        "description": "3.500 UVT — Tope de ingresos brutos para ser responsable de IVA",
        "legal_reference": "Art. 437 del Estatuto Tributario",
    },
    {
        "code": "retefuente_agente_tope",
        "label": "Tope ingresos para ser agente de retención",
        "value_uvt": Decimal("30000"),
        "value_cop": Decimal("30000") * UVT_2025,
        "description": "30.000 UVT — Tope de ingresos brutos o patrimonio para ser agente de retención",
        "legal_reference": "Art. 368 del Estatuto Tributario",
    },
    {
        "code": "exogena_tope",
        "label": "Tope ingresos para reportar información exógena",
        "value_uvt": Decimal("2016"),
        "value_cop": Decimal("2016") * UVT_2025,
        "description": "2.016 UVT — Tope de ingresos brutos para obligación de reportar exógena (aprox.)",
        "legal_reference": "Resolución DIAN vigente para exógena",
    },
]
