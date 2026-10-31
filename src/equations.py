"""ComplexLab Complex Equations Solver
Solves linear equations az + b = c and quadratic equations az^2 + bz + c = 0
with real or complex coefficients.
"""
from typing import Dict, Any, List
import math
from src.complex_engine import ComplexNum, add, subtract, multiply, divide, negate, square_roots, equals
from src.formatter import format_complex, clean_number

TOLERANCE = 1e-9


def solve_linear(a: ComplexNum, b: ComplexNum, c: ComplexNum) -> Dict[str, Any]:
    """Solve linear equation: a*z + b = c for complex z.
    Steps:
    1. Subtract b from both sides: a*z = c - b
    2. Divide both sides by a: z = (c - b) / a
    """
    rhs = subtract(c, b)

    if a.is_zero:
        if rhs.is_zero:
            return {
                "equation": f"({a.formatted()})z + ({b.formatted()}) = {c.formatted()}",
                "solvable": True,
                "infinite_solutions": True,
                "solution": None,
                "explanation": "Because a = 0 and b = c, the equation holds for all complex numbers z (infinitely many solutions)."
            }
        else:
            return {
                "equation": f"({a.formatted()})z + ({b.formatted()}) = {c.formatted()}",
                "solvable": False,
                "infinite_solutions": False,
                "solution": None,
                "explanation": f"Because a = 0 and b ≠ c ({b.formatted()} ≠ {c.formatted()}), there is no solution."
            }

    z = divide(rhs, a)

    steps = [
        {
            "step": 1,
            "title": "Write the initial equation",
            "latex": f"({a.formatted()})z + ({b.formatted()}) = {c.formatted()}"
        },
        {
            "step": 2,
            "title": "Subtract b from both sides",
            "latex": f"({a.formatted()})z = ({c.formatted()}) - ({b.formatted()}) = {rhs.formatted()}"
        },
        {
            "step": 3,
            "title": "Divide by coefficient a",
            "latex": f"z = \\frac{{{rhs.formatted()}}}{{{a.formatted()}}} = {z.formatted()}"
        }
    ]

    return {
        "equation": f"({a.formatted()})z + ({b.formatted()}) = {c.formatted()}",
        "solvable": True,
        "infinite_solutions": False,
        "solution": z.to_dict(),
        "steps": steps
    }


def solve_quadratic(a: ComplexNum, b: ComplexNum, c: ComplexNum) -> Dict[str, Any]:
    """Solve quadratic equation: a*z^2 + b*z + c = 0 with complex coefficients.
    Uses the complex quadratic formula:
    Discriminant: Δ = b^2 - 4ac
    Roots: z = (-b ± sqrt(Δ)) / (2a)
    """
    if a.is_zero:
        # Degenerates to linear equation: b*z + c = 0 -> b*z + c = 0
        lin_res = solve_linear(b, c, ComplexNum(0.0, 0.0))
        lin_res["note"] = "Leading coefficient a = 0, equation reduced to linear."
        return lin_res

    # 1. b^2
    b_sq = multiply(b, b)

    # 2. 4ac
    four = ComplexNum(4.0, 0.0)
    four_a = multiply(four, a)
    four_ac = multiply(four_a, c)

    # 3. Discriminant Δ = b^2 - 4ac
    discriminant = subtract(b_sq, four_ac)

    # 4. Square roots of Δ
    delta_roots = square_roots(discriminant)
    sqrt_delta = delta_roots[0]

    # 5. 2a
    two_a = ComplexNum(2 * a.real, 2 * a.imag)

    # 6. Roots z1 = (-b + sqrt_delta) / 2a, z2 = (-b - sqrt_delta) / 2a
    neg_b = negate(b)
    num1 = add(neg_b, sqrt_delta)
    num2 = subtract(neg_b, sqrt_delta)

    z1 = divide(num1, two_a)
    z2 = divide(num2, two_a)

    is_repeated = equals(z1, z2)

    steps = [
        {
            "step": 1,
            "title": "Identify coefficients",
            "latex": f"a = {a.formatted()}, \\quad b = {b.formatted()}, \\quad c = {c.formatted()}"
        },
        {
            "step": 2,
            "title": "Compute the discriminant: Δ = b² - 4ac",
            "latex": f"\\Delta = ({b.formatted()})^2 - 4({a.formatted()})({c.formatted()}) = {b_sq.formatted()} - ({four_ac.formatted()}) = {discriminant.formatted()}"
        },
        {
            "step": 3,
            "title": "Compute the principal square root of the discriminant: √Δ",
            "latex": f"\\sqrt{{\\Delta}} = \\sqrt{{{discriminant.formatted()}}} = \\pm ({sqrt_delta.formatted()})"
        },
        {
            "step": 4,
            "title": "Apply the quadratic formula: z = (-b ± √Δ) / 2a",
            "latex": f"z = \\frac{{-({b.formatted()}) \\pm ({sqrt_delta.formatted()})}}{{2({a.formatted()})}} = \\frac{{{neg_b.formatted()} \\pm ({sqrt_delta.formatted()})}}{{{two_a.formatted()}}}"
        },
        {
            "step": 5,
            "title": "Calculate the roots",
            "latex": f"z_1 = {z1.formatted()}, \\quad z_2 = {z2.formatted()}"
        }
    ]

    return {
        "equation": f"({a.formatted()})z² + ({b.formatted()})z + ({c.formatted()}) = 0",
        "solvable": True,
        "discriminant": discriminant.to_dict(),
        "sqrt_discriminant": sqrt_delta.to_dict(),
        "is_repeated": is_repeated,
        "roots": [z1.to_dict()] if is_repeated else [z1.to_dict(), z2.to_dict()],
        "steps": steps
    }
