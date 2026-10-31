"""ComplexLab Conversions Module
Handles conversions between Rectangular, Polar, Trigonometric, and Exponential forms,
as well as Degree-Radian conversions.
"""
import math
from typing import Dict, Any, Optional
from src.complex_engine import ComplexNum
from src.formatter import format_complex, format_polar, format_exponential, format_trigonometric, clean_number, angle_to_pi_fraction


def rectangular_to_all(z: ComplexNum, precision: int = 4) -> Dict[str, Any]:
    """Convert rectangular complex number z = a + bi to all representations."""
    r = z.modulus
    theta_rad = z.argument

    if theta_rad is None:
        # Zero complex number
        return {
            "rectangular": z.formatted(precision),
            "real": z.real,
            "imaginary": z.imag,
            "modulus": 0.0,
            "argument_radians": None,
            "argument_degrees": None,
            "polar": "r = 0, θ is undefined",
            "exponential": "0",
            "trigonometric": "0",
            "pi_fraction": None,
            "is_zero": True,
            "note": "For the zero complex number z = 0, the modulus is 0 and the argument (angle) is undefined."
        }

    theta_deg = math.degrees(theta_rad)
    pi_frac = angle_to_pi_fraction(theta_rad)

    return {
        "rectangular": z.formatted(precision),
        "real": round(z.real, precision),
        "imaginary": round(z.imag, precision),
        "modulus": round(r, precision),
        "argument_radians": round(theta_rad, precision),
        "argument_degrees": round(theta_deg, 2),
        "polar": format_polar(r, theta_rad, precision=precision),
        "exponential": format_exponential(r, theta_rad, precision=precision),
        "trigonometric": format_trigonometric(r, theta_rad, precision=precision),
        "pi_fraction": pi_frac,
        "is_zero": False,
        "note": "Principal argument is chosen in the standard interval (-π, π]. Arguments differ by integer multiples of 2π radians."
    }


def polar_to_all(r: float, theta: float, angle_unit: str = "radians", precision: int = 4) -> Dict[str, Any]:
    """Convert polar coordinates (r, theta) to rectangular, exponential, and trigonometric forms."""
    if r < 0:
        raise ValueError("Modulus r cannot be negative in polar coordinates.")

    if angle_unit.lower().startswith("deg"):
        theta_rad = math.radians(theta)
        theta_deg = theta
    else:
        theta_rad = theta
        theta_deg = math.degrees(theta)

    # Normalize theta_rad to (-pi, pi]
    norm_rad = (theta_rad + math.pi) % (2 * math.pi) - math.pi

    if r == 0:
        return rectangular_to_all(ComplexNum(0.0, 0.0), precision)

    z = ComplexNum(r * math.cos(norm_rad), r * math.sin(norm_rad))
    res = rectangular_to_all(z, precision)
    res["input_r"] = r
    res["input_theta"] = theta
    res["input_unit"] = angle_unit
    return res


def convert_angles(value: float, from_unit: str = "degrees") -> Dict[str, Any]:
    """Convert between degrees and radians."""
    if from_unit.lower().startswith("deg"):
        rad = math.radians(value)
        pi_frac = angle_to_pi_fraction(rad)
        return {
            "from_unit": "degrees",
            "to_unit": "radians",
            "degrees": value,
            "radians": round(rad, 6),
            "pi_fraction": pi_frac,
            "formula": f"{value}^\\circ \\times \\frac{{\\pi}}{{180^\\circ}} = {clean_number(rad, 6)}\\text{{ rad}}"
        }
    else:
        deg = math.degrees(value)
        return {
            "from_unit": "radians",
            "to_unit": "degrees",
            "radians": value,
            "degrees": round(deg, 4),
            "formula": f"{value}\\text{{ rad}} \\times \\frac{{180^\\circ}}{{\\pi}} = {clean_number(deg, 4)}^\\circ"
        }
