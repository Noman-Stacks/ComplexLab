"""ComplexLab Roots and Powers Module
Calculates square roots, nth roots, roots of unity, and De Moivre's theorem expansions.
"""
import math
from typing import List, Dict, Any
from src.complex_engine import ComplexNum, nth_roots as calc_nth_roots, square_roots as calc_square_roots
from src.formatter import clean_number, format_complex, format_polar


def get_square_roots_detailed(z: ComplexNum) -> Dict[str, Any]:
    """Calculate the two square roots of z with detailed polar angle steps."""
    if z.is_zero:
        return {
            "input": z.to_dict(),
            "roots": [ComplexNum(0.0, 0.0).to_dict()],
            "modulus_root": 0.0,
            "angle_step_rad": 0.0,
            "is_zero": True
        }

    r = z.modulus
    theta = z.argument
    sqrt_r = math.sqrt(r)

    roots = calc_square_roots(z)
    roots_dict = [root.to_dict() for root in roots]

    return {
        "input": z.to_dict(),
        "roots": roots_dict,
        "modulus_root": sqrt_r,
        "principal_angle_rad": theta / 2.0,
        "second_angle_rad": (theta / 2.0) + math.pi,
        "is_zero": False
    }


def get_nth_roots_detailed(z: ComplexNum, n: int) -> Dict[str, Any]:
    """Calculate all n distinct nth roots of z with polar info for polygon plotting."""
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Root degree n must be a positive integer.")

    if z.is_zero:
        zero_root = ComplexNum(0.0, 0.0).to_dict()
        zero_root["k"] = 0
        zero_root["angle_rad"] = 0.0
        zero_root["angle_deg"] = 0.0
        return {
            "input": z.to_dict(),
            "n": n,
            "roots": [zero_root],
            "root_radius": 0.0,
            "angular_spacing_deg": 360.0 / n if n > 0 else 0.0,
            "is_zero": True
        }

    r = z.modulus
    theta = z.argument
    r_root = r ** (1.0 / n)

    roots_info = []
    for k in range(n):
        angle = (theta + 2 * math.pi * k) / n
        # Normalize to (-pi, pi]
        norm_angle = (angle + math.pi) % (2 * math.pi) - math.pi
        root_num = ComplexNum(r_root * math.cos(angle), r_root * math.sin(angle))
        root_dict = root_num.to_dict()
        root_dict["k"] = k
        root_dict["angle_rad"] = round(norm_angle, 6)
        root_dict["angle_deg"] = round(math.degrees(norm_angle), 2)
        root_dict["polar"] = format_polar(r_root, norm_angle)
        roots_info.append(root_dict)

    return {
        "input": z.to_dict(),
        "n": n,
        "roots": roots_info,
        "root_radius": round(r_root, 6),
        "angular_spacing_rad": 2 * math.pi / n,
        "angular_spacing_deg": round(360.0 / n, 2),
        "is_zero": False
    }


def get_roots_of_unity_detailed(n: int) -> Dict[str, Any]:
    """Calculate the n nth roots of unity (solutions of z^n = 1)."""
    one = ComplexNum(1.0, 0.0)
    data = get_nth_roots_detailed(one, n)
    data["title"] = f"{n}-th Roots of Unity"
    return data


def apply_de_moivre(z: ComplexNum, n: int) -> Dict[str, Any]:
    """Apply De Moivre's theorem: [r(cos θ + i sin θ)]^n = r^n (cos nθ + i sin nθ)."""
    if z.is_zero:
        if n < 0:
            raise ZeroDivisionError("Cannot raise zero to a negative exponent.")
        res = ComplexNum(0.0, 0.0) if n > 0 else ComplexNum(1.0, 0.0)
        return {
            "input": z.to_dict(),
            "n": n,
            "r": 0.0,
            "theta": 0.0,
            "r_pow_n": 0.0 if n > 0 else 1.0,
            "n_theta": 0.0,
            "result": res.to_dict()
        }

    r = z.modulus
    theta = z.argument
    r_n = r ** n
    n_theta = theta * n
    # Normalized angle to (-pi, pi]
    norm_n_theta = (n_theta + math.pi) % (2 * math.pi) - math.pi
    res = ComplexNum(r_n * math.cos(n_theta), r_n * math.sin(n_theta))

    return {
        "input": z.to_dict(),
        "n": n,
        "r": round(r, 6),
        "theta_rad": round(theta, 6),
        "theta_deg": round(math.degrees(theta), 2),
        "r_pow_n": round(r_n, 6),
        "n_theta_rad": round(norm_n_theta, 6),
        "n_theta_deg": round(math.degrees(norm_n_theta), 2),
        "result": res.to_dict()
    }
