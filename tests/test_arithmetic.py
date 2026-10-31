"""Tests for Basic Complex Arithmetic Operations & Identities
"""
import pytest
from src.complex_engine import (
    ComplexNum, add, subtract, multiply, divide, negate, equals,
    sum_multiple, product_multiple
)


def test_addition():
    z1 = ComplexNum(3.0, 4.0)
    z2 = ComplexNum(1.0, -2.0)
    res = add(z1, z2)
    assert res.real == 4.0
    assert res.imag == 2.0


def test_subtraction():
    z1 = ComplexNum(5.0, 7.0)
    z2 = ComplexNum(2.0, 3.0)
    res = subtract(z1, z2)
    assert res.real == 3.0
    assert res.imag == 4.0


def test_multiplication():
    # (3 + 4i)(2 - i) = 6 - 3i + 8i - 4(-1) = 10 + 5i
    z1 = ComplexNum(3.0, 4.0)
    z2 = ComplexNum(2.0, -1.0)
    res = multiply(z1, z2)
    assert res.real == 10.0
    assert res.imag == 5.0


def test_division():
    # (3 + 4i) / (1 - 2i) = -1 + 2i
    z1 = ComplexNum(3.0, 4.0)
    z2 = ComplexNum(1.0, -2.0)
    res = divide(z1, z2)
    assert abs(res.real - (-1.0)) < 1e-9
    assert abs(res.imag - 2.0) < 1e-9


def test_division_by_zero():
    z1 = ComplexNum(3.0, 4.0)
    z2 = ComplexNum(0.0, 0.0)
    with pytest.raises(ZeroDivisionError):
        divide(z1, z2)


def test_negation():
    z = ComplexNum(3.0, -4.5)
    neg = negate(z)
    assert neg.real == -3.0
    assert neg.imag == 4.5


def test_equality():
    z1 = ComplexNum(2.5, -1.1)
    z2 = ComplexNum(2.5, -1.1)
    z3 = ComplexNum(2.5, 1.1)
    assert equals(z1, z2)
    assert not equals(z1, z3)


def test_multi_sum_and_product():
    nums = [ComplexNum(1, 2), ComplexNum(3, -1), ComplexNum(-2, 4)]
    total_sum = sum_multiple(nums)
    assert total_sum.real == 2.0
    assert total_sum.imag == 5.0

    total_prod = product_multiple([ComplexNum(1, 1), ComplexNum(1, -1), ComplexNum(2, 0)])
    # (1+i)(1-i) = 2, * 2 = 4
    assert total_prod.real == 4.0
    assert abs(total_prod.imag) < 1e-9


def test_modulus_multiplication_identity():
    # |z1 * z2| = |z1| * |z2|
    z1 = ComplexNum(3.0, 4.0)  # |z1| = 5
    z2 = ComplexNum(1.0, 2.0)  # |z2| = sqrt(5)
    prod = multiply(z1, z2)
    assert abs(prod.modulus - (z1.modulus * z2.modulus)) < 1e-9
