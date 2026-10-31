"""Tests for Modulus, Principal Argument, Reciprocal, and Angle Identities
"""
import pytest
import math
from src.complex_engine import (
    ComplexNum, modulus, argument, reciprocal, normalize,
    verify_multiplicative_inverse, multiply
)


def test_modulus():
    z1 = ComplexNum(3.0, 4.0)
    assert abs(modulus(z1) - 5.0) < 1e-9

    z2 = ComplexNum(0.0, -7.0)
    assert abs(modulus(z2) - 7.0) < 1e-9

    z3 = ComplexNum(0.0, 0.0)
    assert modulus(z3) == 0.0


def test_argument_quadrants():
    # Quadrant I: (1, 1) -> 45 deg = pi/4
    z1 = ComplexNum(1.0, 1.0)
    rad1, deg1 = argument(z1)
    assert abs(rad1 - (math.pi / 4)) < 1e-6
    assert abs(deg1 - 45.0) < 1e-6

    # Quadrant II: (-1, 1) -> 135 deg = 3pi/4
    z2 = ComplexNum(-1.0, 1.0)
    rad2, deg2 = argument(z2)
    assert abs(rad2 - (3 * math.pi / 4)) < 1e-6
    assert abs(deg2 - 135.0) < 1e-6

    # Quadrant III: (-1, -1) -> -135 deg = -3pi/4
    z3 = ComplexNum(-1.0, -1.0)
    rad3, deg3 = argument(z3)
    assert abs(rad3 - (-3 * math.pi / 4)) < 1e-6
    assert abs(deg3 - (-135.0)) < 1e-6

    # Quadrant IV: (1, -1) -> -45 deg = -pi/4
    z4 = ComplexNum(1.0, -1.0)
    rad4, deg4 = argument(z4)
    assert abs(rad4 - (-math.pi / 4)) < 1e-6
    assert abs(deg4 - (-45.0)) < 1e-6


def test_argument_zero_is_undefined():
    z_zero = ComplexNum(0.0, 0.0)
    rad, deg = argument(z_zero)
    assert rad is None
    assert deg is None


def test_reciprocal_and_identity():
    # (3 + 4i)^(-1) = (3 - 4i)/25 = 0.12 - 0.16i
    z = ComplexNum(3.0, 4.0)
    inv = reciprocal(z)
    assert abs(inv.real - 0.12) < 1e-9
    assert abs(inv.imag - (-0.16)) < 1e-9

    # Identity z * z^(-1) = 1
    prod = multiply(z, inv)
    assert abs(prod.real - 1.0) < 1e-9
    assert abs(prod.imag) < 1e-9

    res = verify_multiplicative_inverse(z)
    assert res["verified"] is True


def test_reciprocal_of_zero():
    z = ComplexNum(0.0, 0.0)
    with pytest.raises(ZeroDivisionError):
        reciprocal(z)


def test_normalize():
    z = ComplexNum(3.0, 4.0)
    unit_z = normalize(z)
    assert abs(unit_z.modulus - 1.0) < 1e-9
    assert abs(unit_z.real - 0.6) < 1e-9
    assert abs(unit_z.imag - 0.8) < 1e-9

    with pytest.raises(ZeroDivisionError):
        normalize(ComplexNum(0.0, 0.0))


def test_argument_product_identity():
    # arg(z1 * z2) = arg(z1) + arg(z2) (mod 2pi)
    z1 = ComplexNum(1.0, 1.0)  # pi/4
    z2 = ComplexNum(0.0, 2.0)  # pi/2
    prod = multiply(z1, z2)

    arg1, _ = argument(z1)
    arg2, _ = argument(z2)
    arg_prod, _ = argument(prod)

    expected = (arg1 + arg2 + math.pi) % (2 * math.pi) - math.pi
    assert abs(arg_prod - expected) < 1e-9
