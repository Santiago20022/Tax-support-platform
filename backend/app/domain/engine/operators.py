"""Operator implementations for rule condition evaluation."""
from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation


def _to_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _to_list(value: object) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        return [v.strip() for v in value.split(",")]
    return [value]


def op_gt(profile_value: object, threshold_value: object) -> bool:
    pv = _to_decimal(profile_value)
    tv = _to_decimal(threshold_value)
    if pv is None or tv is None:
        return False
    return pv > tv


def op_gte(profile_value: object, threshold_value: object) -> bool:
    pv = _to_decimal(profile_value)
    tv = _to_decimal(threshold_value)
    if pv is None or tv is None:
        return False
    return pv >= tv


def op_lt(profile_value: object, threshold_value: object) -> bool:
    pv = _to_decimal(profile_value)
    tv = _to_decimal(threshold_value)
    if pv is None or tv is None:
        return False
    return pv < tv


def op_lte(profile_value: object, threshold_value: object) -> bool:
    pv = _to_decimal(profile_value)
    tv = _to_decimal(threshold_value)
    if pv is None or tv is None:
        return False
    return pv <= tv


def op_eq(profile_value: object, threshold_value: object) -> bool:
    pv_dec = _to_decimal(profile_value)
    tv_dec = _to_decimal(threshold_value)
    if pv_dec is not None and tv_dec is not None:
        return pv_dec == tv_dec
    return str(profile_value).strip().lower() == str(threshold_value).strip().lower()


def op_neq(profile_value: object, threshold_value: object) -> bool:
    return not op_eq(profile_value, threshold_value)


def op_in(profile_value: object, threshold_value: object) -> bool:
    value_list = _to_list(threshold_value)
    normalized = [str(v).strip().lower() for v in value_list]
    return str(profile_value).strip().lower() in normalized


def op_not_in(profile_value: object, threshold_value: object) -> bool:
    return not op_in(profile_value, threshold_value)


def op_between(
    profile_value: object,
    threshold_value: object,
    threshold_value_secondary: object = None,
) -> bool:
    pv = _to_decimal(profile_value)
    low = _to_decimal(threshold_value)
    high = _to_decimal(threshold_value_secondary)
    if pv is None or low is None or high is None:
        return False
    return low <= pv <= high


def op_is_true(profile_value: object, threshold_value: object = None) -> bool:
    if isinstance(profile_value, bool):
        return profile_value is True
    return str(profile_value).strip().lower() in ("true", "1", "yes")


def op_is_false(profile_value: object, threshold_value: object = None) -> bool:
    if isinstance(profile_value, bool):
        return profile_value is False
    return str(profile_value).strip().lower() in ("false", "0", "no")


OPERATORS: dict[str, callable] = {
    "gt": op_gt,
    "gte": op_gte,
    "lt": op_lt,
    "lte": op_lte,
    "eq": op_eq,
    "neq": op_neq,
    "in": op_in,
    "not_in": op_not_in,
    "between": op_between,
    "is_true": op_is_true,
    "is_false": op_is_false,
}


def apply_operator(
    operator: str,
    profile_value: object,
    threshold_value: object,
    threshold_value_secondary: object = None,
) -> bool:
    op_func = OPERATORS.get(operator)
    if op_func is None:
        raise ValueError(f"Unknown operator: {operator}")
    if operator == "between":
        return op_func(profile_value, threshold_value, threshold_value_secondary)
    return op_func(profile_value, threshold_value)
