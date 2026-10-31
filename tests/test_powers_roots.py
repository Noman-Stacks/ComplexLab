"""Tests for Powers, Powers of i, Square Roots, Nth Roots, Roots of Unity, and De Moivre
"""
import pytest
import math
from src.complex_engine import (
    ComplexNum, integer_power, powers_of_i, square_roots, nth_roots,
    roots_of_unity, equals, multiply
)
from src.roots import get_nth_roots_detailed, apply_de_moivre


def test_integer_power():
    # (1 + i)^2 = 2i
    z = ComplexNum(1.0, 1.0)
    p2 = integer_power(z, 2)
    assert abs(p2.real - 0.0) < 1e-9
    assert abs(p2.imag - 2.0) < 1e-9

    # (1 + i)^8 = 16
    p8 = integer_power(z, 8)
    assert abs(p8.real - 16.0) < 1e-9
    assert abs(p8.imag - 0.0) < 1e-9

    # z^0 = 1
    p0 = integer_power(z, 0)
    assert p0 == ComplexNum(1.0, 0.0)

    # Negative integer power: (2i)^(-1) = -0.5i
    z2 = ComplexNum(0.0, 2.0)
    p_neg1 = integer_power(z2, -1)
    assert abs(p_neg1.real) < 1e-9
    assert abs(p_neg1.imag - (-0.5)) < 1e-9


def test_powers_of_i():
    assert powers_of_i(0)["result_str"] == "1"
    assert powers_of_i(1)["result_str"] == "i"
    assert powers_of_i(2)["result_str"] == "-1"
    assert powers_of_i(3)["result_str"] == "-i"
    assert powers_of_i(4)["result_str"] == "1"
    assert powers_of_i(100)["result_str"] == "1"
    assert powers_of_i(105)["result_str"] == "i"


def test_square_roots():
    # Square roots of -4: +2i and -2i
    z = ComplexNum(-4.0, 0.0)
    roots = square_roots(z)
    assert len(roots) == 2

    # Verify both roots squared give z
    for r in roots:
        r_sq = multiply(r, r)
        assert abs(r_sq.real - (-4.0)) < 1e-9
        assert abs(r_sq.imag) < 1e-9

    # Principal square root of -4 is 2i
    assert abs(roots[0].real) < 1e-9
    assert abs(roots[0].imag - 2.0) < 1e-9


def test_nth_roots_and_spacing():
    # 4th roots of 16: radius = 2, angles = 0, pi/2, pi, -pi/2
    z = ComplexNum(16.0, 0.0)
    roots = nth_roots(z, 4)
    assert len(roots) == 4
    for r in roots:
        assert abs(r.modulus - 2.0) < 1e-9

    details = get_nth_roots_detailed(z, 4)
    assert details["root_radius"] == 2.0
    assert details["angular_spacing_deg"] == 90.0


def test_roots_of_unity():
    # Cube roots of unity: sum of roots = 0
    roots3 = roots_of_unity(3)
    assert len(roots3) == 3
    sum_real = sum(r.real for r in roots3)
    sum_imag = sum(r.imag for r in roots3)
    assert abs(sum_real) < 1e-9
    assert abs(sum_imag) < 1e-9


def test_de_moivre():
    z = ComplexNum(1.0, 1.0)
    data = apply_de_moivre(z, 4)
    # (1+i)^4 = -4
    res = data["result"]
    assert abs(res["real"] - (-4.0)) < 1e-9
    assert abs(res["imaginary"]) < 1e-9
