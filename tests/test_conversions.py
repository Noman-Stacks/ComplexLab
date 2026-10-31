"""Tests for Rectangular, Polar, Trigonometric, Exponential, and Degree-Radian Conversions
"""
import math
from src.complex_engine import ComplexNum
from src.conversions import rectangular_to_all, polar_to_all, convert_angles
from src.formatter import format_complex, clean_number, angle_to_pi_fraction


def test_rectangular_to_polar_and_back():
    z = ComplexNum(3.0, 4.0)
    data = rectangular_to_all(z)
    assert abs(data["modulus"] - 5.0) < 1e-4

    # Round trip polar back to rectangular
    back = polar_to_all(data["modulus"], data["argument_radians"])
    assert abs(back["real"] - 3.0) < 1e-4
    assert abs(back["imaginary"] - 4.0) < 1e-4


def test_zero_complex_conversions():
    z_zero = ComplexNum(0.0, 0.0)
    data = rectangular_to_all(z_zero)
    assert data["is_zero"] is True
    assert data["modulus"] == 0.0
    assert data["argument_radians"] is None


def test_degree_radian_conversion():
    d2r = convert_angles(180, from_unit="degrees")
    assert abs(d2r["radians"] - math.pi) < 1e-6

    r2d = convert_angles(math.pi / 2, from_unit="radians")
    assert abs(r2d["degrees"] - 90.0) < 1e-6


def test_formatting_rules():
    assert format_complex(0, 0) == "0"
    assert format_complex(3, 0) == "3"
    assert format_complex(0, 4) == "4i"
    assert format_complex(0, -4) == "-4i"
    assert format_complex(0, 1) == "i"
    assert format_complex(0, -1) == "-i"
    assert format_complex(3, 1) == "3 + i"
    assert format_complex(3, -1) == "3 - i"
    assert format_complex(3, 4) == "3 + 4i"
    assert format_complex(3, -4) == "3 - 4i"


def test_pi_fractions():
    assert angle_to_pi_fraction(math.pi / 4) == r"\frac{\pi}{4}"
    assert angle_to_pi_fraction(math.pi / 2) == r"\frac{\pi}{2}"
    assert angle_to_pi_fraction(math.pi) == r"\pi"
    assert angle_to_pi_fraction(-math.pi / 2) == r"-\frac{\pi}{2}"
