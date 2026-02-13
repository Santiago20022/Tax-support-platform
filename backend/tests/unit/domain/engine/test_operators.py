"""Tests for rule condition operators."""

from decimal import Decimal

import pytest

from app.domain.engine.operators import apply_operator


class TestNumericOperators:
    def test_gt_true(self):
        assert apply_operator("gt", Decimal("100"), Decimal("50")) is True

    def test_gt_false_equal(self):
        assert apply_operator("gt", Decimal("50"), Decimal("50")) is False

    def test_gt_false_less(self):
        assert apply_operator("gt", Decimal("30"), Decimal("50")) is False

    def test_gte_true_greater(self):
        assert apply_operator("gte", Decimal("100"), Decimal("50")) is True

    def test_gte_true_equal(self):
        assert apply_operator("gte", Decimal("50"), Decimal("50")) is True

    def test_gte_false(self):
        assert apply_operator("gte", Decimal("30"), Decimal("50")) is False

    def test_lt_true(self):
        assert apply_operator("lt", Decimal("30"), Decimal("50")) is True

    def test_lt_false(self):
        assert apply_operator("lt", Decimal("100"), Decimal("50")) is False

    def test_lte_true_equal(self):
        assert apply_operator("lte", Decimal("50"), Decimal("50")) is True

    def test_lte_true_less(self):
        assert apply_operator("lte", Decimal("30"), Decimal("50")) is True

    def test_lte_false(self):
        assert apply_operator("lte", Decimal("100"), Decimal("50")) is False

    def test_between_true(self):
        assert apply_operator("between", Decimal("50"), Decimal("10"), Decimal("100")) is True

    def test_between_true_boundaries(self):
        assert apply_operator("between", Decimal("10"), Decimal("10"), Decimal("100")) is True
        assert apply_operator("between", Decimal("100"), Decimal("10"), Decimal("100")) is True

    def test_between_false(self):
        assert apply_operator("between", Decimal("200"), Decimal("10"), Decimal("100")) is False

    def test_none_value_returns_false(self):
        assert apply_operator("gte", None, Decimal("50")) is False
        assert apply_operator("gt", Decimal("50"), None) is False


class TestEqualityOperators:
    def test_eq_string(self):
        assert apply_operator("eq", "ordinario", "ordinario") is True

    def test_eq_string_case_insensitive(self):
        assert apply_operator("eq", "Ordinario", "ordinario") is True

    def test_eq_numeric(self):
        assert apply_operator("eq", Decimal("100"), Decimal("100")) is True

    def test_neq_true(self):
        assert apply_operator("neq", "simple", "ordinario") is True

    def test_neq_false(self):
        assert apply_operator("neq", "ordinario", "ordinario") is False


class TestMembershipOperators:
    def test_in_list(self):
        assert apply_operator("in", "Bogotá", '["Bogotá", "Medellín"]') is True

    def test_in_list_not_found(self):
        assert apply_operator("in", "Cali", '["Bogotá", "Medellín"]') is False

    def test_not_in_list(self):
        assert apply_operator("not_in", "Cali", '["Bogotá", "Medellín"]') is True

    def test_in_comma_separated(self):
        assert apply_operator("in", "Bogotá", "Bogotá, Medellín, Cali") is True


class TestBooleanOperators:
    def test_is_true_with_bool(self):
        assert apply_operator("is_true", True, None) is True

    def test_is_true_with_false(self):
        assert apply_operator("is_true", False, None) is False

    def test_is_true_with_string(self):
        assert apply_operator("is_true", "true", None) is True

    def test_is_false_with_bool(self):
        assert apply_operator("is_false", False, None) is True

    def test_is_false_with_true(self):
        assert apply_operator("is_false", True, None) is False


class TestInvalidOperator:
    def test_unknown_operator_raises(self):
        with pytest.raises(ValueError, match="Unknown operator"):
            apply_operator("unknown_op", 1, 2)
