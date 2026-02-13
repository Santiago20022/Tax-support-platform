"""Seed data for obligation types catalog."""

OBLIGATION_TYPES = [
    {
        "code": "renta",
        "name": "Impuesto sobre la Renta y Complementarios",
        "category": "nacional",
        "description": (
            "Impuesto anual sobre los ingresos de personas naturales y jurídicas. "
            "Las personas naturales deben declarar si superan ciertos topes de ingresos, "
            "patrimonio, consignaciones bancarias o compras con tarjeta."
        ),
        "responsible_entity": "DIAN",
        "legal_base": "Art. 592 del Estatuto Tributario; Art. 593 del Estatuto Tributario",
        "display_order": 1,
    },
    {
        "code": "iva",
        "name": "Impuesto sobre las Ventas (IVA)",
        "category": "nacional",
        "description": (
            "Impuesto al consumo que grava la venta de bienes y servicios. "
            "Los responsables de IVA deben presentar declaración bimestral o cuatrimestral "
            "según el nivel de ingresos."
        ),
        "responsible_entity": "DIAN",
        "legal_base": "Art. 437 del Estatuto Tributario; Art. 600 del Estatuto Tributario",
        "display_order": 2,
    },
    {
        "code": "ica",
        "name": "Industria y Comercio (ICA)",
        "category": "territorial",
        "description": (
            "Impuesto municipal que grava las actividades industriales, comerciales y "
            "de servicios realizadas en un municipio. La periodicidad y tarifas varían "
            "según el municipio."
        ),
        "responsible_entity": "Secretaría de Hacienda Municipal",
        "legal_base": "Acuerdo 65 de 2002 - Bogotá; Decreto 352 de 2002",
        "display_order": 3,
    },
    {
        "code": "retefuente",
        "name": "Retención en la Fuente",
        "category": "nacional",
        "description": (
            "Mecanismo de recaudo anticipado del impuesto de renta. Los agentes de "
            "retención deben practicar, declarar y pagar las retenciones mensualmente."
        ),
        "responsible_entity": "DIAN",
        "legal_base": "Art. 368 del Estatuto Tributario",
        "display_order": 4,
    },
    {
        "code": "nomina_seguridad_social",
        "name": "Nómina y Seguridad Social",
        "category": "laboral",
        "description": (
            "Obligación de realizar el pago mensual de aportes a seguridad social "
            "(salud, pensión, ARL) y parafiscales a través de la planilla PILA "
            "cuando se tienen empleados."
        ),
        "responsible_entity": "Operadores PILA",
        "legal_base": "Ley 100 de 1993; Ley 1607 de 2012",
        "display_order": 5,
    },
    {
        "code": "exogena",
        "name": "Información Exógena",
        "category": "nacional",
        "description": (
            "Obligación de reportar información a la DIAN sobre operaciones con "
            "terceros cuando se superan los topes establecidos por resolución."
        ),
        "responsible_entity": "DIAN",
        "legal_base": "Resolución DIAN vigente para información exógena",
        "display_order": 6,
    },
]
