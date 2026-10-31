"""Tests for Conjugate Operations and Textbook Conjugate Identities
"""
from src.complex_engine import (
    ComplexNum, conjugate, double_conjugate, real_part, imag_part,
    verify_conjugate_identities, product_with_conjugate
)


def test_conjugate():
    z1 = ComplexNum(3.0, 4.0)
    assert conjugate(z1) == ComplexNum(3.0, -4.0)

    z2 = ComplexNum(-2.5, -6.0)
    assert conjugate(z2) == ComplexNum(-2.5, 6.0)


def test_double_conjugate():
    z = ComplexNum(7.0, -9.0)
    conj2, is_identity = double_conjugate(z)
    assert conj2 == z
    assert is_identity is True


def test_real_and_imag_parts():
    z = ComplexNum(-8.25, 14.5)
    assert real_part(z) == -8.25
    assert imag_part(z) == 14.5


def test_conjugate_identities():
    """Verify:
    1. z + z̄ = 2·Re(z)
    2. z - z̄ = 2i·Im(z)
    3. z · z̄ = |z|²
    """
    z = ComplexNum(3.0, -4.0)
    ids = verify_conjugate_identities(z)
    assert ids["identity_1"]["holds"] is True
    assert ids["identity_2"]["holds"] is True
    assert ids["identity_3"]["holds"] is True


def test_product_with_conjugate():
    z = ComplexNum(3.0, 4.0)
    res = product_with_conjugate(z)
    assert res["is_real"] is True
    assert abs(res["modulus_squared"] - 25.0) < 1e-9
    assert abs(res["product"]["real"] - 25.0) < 1e-9
    assert abs(res["product"]["imaginary"] - 0.0) < 1e-9
