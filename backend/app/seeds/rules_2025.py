"""Seed data for rules fiscal year 2025."""

RULES_2025 = [
    # --- RENTA ---
    {
        "obligation_code": "renta",
        "code": "renta_pn_ingresos_brutos",
        "name": "Renta por ingresos brutos, patrimonio, consignaciones o compras superiores al tope",
        "description": "Evalúa si la persona natural supera alguno de los topes para declarar renta",
        "logic_operator": "OR",
        "priority": 1,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "ingresos_brutos_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "renta_pn_ingresos_tope",
                "description": "Ingresos brutos >= 1.400 UVT",
            },
            {
                "field": "patrimonio_bruto_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "renta_pn_patrimonio_tope",
                "description": "Patrimonio bruto >= 4.500 UVT",
            },
            {
                "field": "consignaciones_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "renta_pn_consignaciones_tope",
                "description": "Consignaciones bancarias >= 1.400 UVT",
            },
            {
                "field": "compras_consumos_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "renta_pn_compras_tope",
                "description": "Compras y consumos tarjeta >= 1.400 UVT",
            },
        ],
    },
    # --- IVA ---
    {
        "obligation_code": "iva",
        "code": "iva_responsable_ingresos",
        "name": "Responsable de IVA por ingresos y actividad gravada",
        "description": "Evalúa si es responsable de IVA por régimen ordinario e ingresos superiores al tope",
        "logic_operator": "AND",
        "priority": 1,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "regime",
                "operator": "eq",
                "value_type": "literal",
                "value": "ordinario",
                "description": "Régimen ordinario",
            },
            {
                "field": "ingresos_brutos_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "iva_responsable_tope",
                "description": "Ingresos brutos >= 3.500 UVT",
            },
        ],
    },
    {
        "obligation_code": "iva",
        "code": "iva_responsable_declarado",
        "name": "Responsable de IVA declarado explícitamente",
        "description": "Si el usuario indica que ya es responsable de IVA",
        "logic_operator": "AND",
        "priority": 2,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "is_iva_responsable",
                "operator": "is_true",
                "value_type": "literal",
                "value": "true",
                "description": "Es responsable de IVA",
            },
        ],
    },
    # --- ICA ---
    {
        "obligation_code": "ica",
        "code": "ica_actividad_comercial",
        "name": "ICA por actividad comercial en municipio",
        "description": "Evalúa si tiene actividad comercial registrada en un municipio",
        "logic_operator": "AND",
        "priority": 1,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "has_comercio_registration",
                "operator": "is_true",
                "value_type": "literal",
                "value": "true",
                "description": "Tiene registro de comercio",
            },
            {
                "field": "city",
                "operator": "neq",
                "value_type": "literal",
                "value": "",
                "description": "Tiene ciudad de operación definida",
            },
        ],
    },
    # --- RETENCIÓN EN LA FUENTE ---
    {
        "obligation_code": "retefuente",
        "code": "retefuente_agente_ingresos",
        "name": "Agente de retención por ingresos o patrimonio",
        "description": "Evalúa si cumple topes para ser agente de retención",
        "logic_operator": "AND",
        "priority": 1,
        "result_if_true": "conditional",
        "conditions": [
            {
                "field": "regime",
                "operator": "eq",
                "value_type": "literal",
                "value": "ordinario",
                "description": "Régimen ordinario",
            },
            {
                "field": "ingresos_brutos_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "retefuente_agente_tope",
                "description": "Ingresos brutos >= 30.000 UVT",
            },
        ],
    },
    # --- NÓMINA Y SEGURIDAD SOCIAL ---
    {
        "obligation_code": "nomina_seguridad_social",
        "code": "nomina_empleados",
        "name": "Nómina y seguridad social por tener empleados",
        "description": "Si tiene empleados, debe cumplir con PILA",
        "logic_operator": "AND",
        "priority": 1,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "has_employees",
                "operator": "is_true",
                "value_type": "literal",
                "value": "true",
                "description": "Tiene empleados",
            },
            {
                "field": "employee_count",
                "operator": "gt",
                "value_type": "literal",
                "value": "0",
                "description": "Número de empleados > 0",
            },
        ],
    },
    # --- INFORMACIÓN EXÓGENA ---
    {
        "obligation_code": "exogena",
        "code": "exogena_ingresos_tope",
        "name": "Información exógena por ingresos superiores al tope",
        "description": "Evalúa si debe reportar información exógena por nivel de ingresos",
        "logic_operator": "OR",
        "priority": 1,
        "result_if_true": "applies",
        "conditions": [
            {
                "field": "ingresos_brutos_cop",
                "operator": "gte",
                "value_type": "threshold_ref",
                "value": "exogena_tope",
                "description": "Ingresos brutos >= tope exógena",
            },
        ],
    },
]
