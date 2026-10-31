"""ComplexLab Step-by-Step Explanations Generator
Generates detailed, pedagogically sound mathematical explanations and LaTeX steps
for every complex number operation.
"""
import math
from typing import List, Dict, Any
from src.complex_engine import ComplexNum, conjugate as calc_conj
from src.formatter import clean_number, format_complex, angle_to_pi_fraction


def explain_addition(z1: ComplexNum, z2: ComplexNum, res: ComplexNum) -> List[Dict[str, str]]:
    return [
        {
            "step": "1",
            "title": "State the addition of the two complex numbers",
            "latex": f"z_1 + z_2 = ({z1.formatted()}) + ({z2.formatted()})"
        },
        {
            "step": "2",
            "title": "Group the real components and imaginary components",
            "latex": f"= ({clean_number(z1.real)} + {clean_number(z2.real)}) + ({clean_number(z1.imag)} + {clean_number(z2.imag)})i"
        },
        {
            "step": "3",
            "title": "Perform the additions",
            "latex": f"= {clean_number(res.real)} + ({clean_number(res.imag)})i"
        },
        {
            "step": "4",
            "title": "Final Result",
            "latex": f"z_1 + z_2 = {res.formatted()}"
        }
    ]


def explain_subtraction(z1: ComplexNum, z2: ComplexNum, res: ComplexNum) -> List[Dict[str, str]]:
    return [
        {
            "step": "1",
            "title": "State the subtraction of the two complex numbers",
            "latex": f"z_1 - z_2 = ({z1.formatted()}) - ({z2.formatted()})"
        },
        {
            "step": "2",
            "title": "Distribute the negative sign across z₂",
            "latex": f"= ({z1.formatted()}) + ({-z2.real:+g} {-z2.imag:+g}i)".replace("+-", "-")
        },
        {
            "step": "3",
            "title": "Group real and imaginary parts",
            "latex": f"= ({clean_number(z1.real)} - ({clean_number(z2.real)})) + ({clean_number(z1.imag)} - ({clean_number(z2.imag)}))i"
        },
        {
            "step": "4",
            "title": "Final Result",
            "latex": f"z_1 - z_2 = {res.formatted()}"
        }
    ]


def explain_multiplication(z1: ComplexNum, z2: ComplexNum, res: ComplexNum) -> List[Dict[str, str]]:
    a, b = z1.real, z1.imag
    c, d = z2.real, z2.imag
    ac = a * c
    ad = a * d
    bc = b * c
    bd = b * d
    real_part = ac - bd
    imag_part = ad + bc

    return [
        {
            "step": "1",
            "title": "Write the expression as a binomial product",
            "latex": f"({z1.formatted()}) \\times ({z2.formatted()})"
        },
        {
            "step": "2",
            "title": "Apply the distributive property (FOIL)",
            "latex": f"= ({clean_number(a)} \\cdot {clean_number(c)}) + ({clean_number(a)} \\cdot {clean_number(d)}i) + ({clean_number(b)}i \\cdot {clean_number(c)}) + ({clean_number(b)}i \\cdot {clean_number(d)}i)"
        },
        {
            "step": "3",
            "title": "Multiply individual terms",
            "latex": f"= {clean_number(ac)} + ({clean_number(ad)}i) + ({clean_number(bc)}i) + ({clean_number(bd)}i^2)"
        },
        {
            "step": "4",
            "title": "Substitute the fundamental identity i² = -1",
            "latex": f"= {clean_number(ac)} + ({clean_number(ad + bc)}i) + ({clean_number(bd)}(-1)) = {clean_number(ac)} - ({clean_number(bd)}) + ({clean_number(ad + bc)}i)"
        },
        {
            "step": "5",
            "title": "Combine real and imaginary parts",
            "latex": f"= {res.formatted()}"
        }
    ]


def explain_division(z1: ComplexNum, z2: ComplexNum, res: ComplexNum) -> List[Dict[str, str]]:
    z2_conj = calc_conj(z2)
    denom = z2.real**2 + z2.imag**2

    return [
        {
            "step": "1",
            "title": "Write the fraction",
            "latex": f"\\frac{{z_1}}{{z_2}} = \\frac{{{z1.formatted()}}}{{{z2.formatted()}}}"
        },
        {
            "step": "2",
            "title": "Determine the complex conjugate of the denominator",
            "latex": f"\\overline{{z_2}} = \\overline{{{z2.formatted()}}} = {z2_conj.formatted()}"
        },
        {
            "step": "3",
            "title": "Multiply numerator and denominator by the conjugate to realize the denominator",
            "latex": f"= \\frac{{({z1.formatted()})({z2_conj.formatted()})}}{{({z2.formatted()})({z2_conj.formatted()})}}"
        },
        {
            "step": "4",
            "title": "Expand numerator and denominator using z · z̄ = |z|²",
            "latex": f"\\text{{Denominator: }} ({clean_number(z2.real)})^2 + ({clean_number(z2.imag)})^2 = {clean_number(denom)}"
        },
        {
            "step": "5",
            "title": "Expand the numerator",
            "latex": f"\\text{{Numerator: }} ({z1.formatted()})({z2_conj.formatted()}) = {clean_number(res.real * denom)} + ({clean_number(res.imag * denom)}i)"
        },
        {
            "step": "6",
            "title": "Divide each term by the real denominator",
            "latex": f"= \\frac{{{clean_number(res.real * denom)}}}{{{clean_number(denom)}}} + \\frac{{{clean_number(res.imag * denom)}}}{{{clean_number(denom)}}}i = {res.formatted()}"
        }
    ]


def explain_modulus(z: ComplexNum, mod: float) -> List[Dict[str, str]]:
    a, b = z.real, z.imag
    a_sq = a ** 2
    b_sq = b ** 2
    sum_sq = a_sq + b_sq

    return [
        {
            "step": "1",
            "title": "Recall the modulus (absolute value) formula",
            "latex": "|z| = \\sqrt{a^2 + b^2} \\quad \\text{where } z = a + bi"
        },
        {
            "step": "2",
            "title": "Substitute real part a and imaginary part b",
            "latex": f"|z| = \\sqrt{{({clean_number(a)})^2 + ({clean_number(b)})^2}}"
        },
        {
            "step": "3",
            "title": "Square both components",
            "latex": f"= \\sqrt{{{clean_number(a_sq)} + {clean_number(b_sq)}}}"
        },
        {
            "step": "4",
            "title": "Sum the squares and compute the square root",
            "latex": f"= \\sqrt{{{clean_number(sum_sq)}}} \\approx {clean_number(mod, 6)}"
        }
    ]


def explain_argument(z: ComplexNum, arg_rad: float, arg_deg: float) -> List[Dict[str, str]]:
    a, b = z.real, z.imag
    if z.is_zero:
        return [
            {
                "step": "1",
                "title": "Evaluate argument of zero",
                "latex": "\\text{arg}(0) \\text{ is undefined.}"
            },
            {
                "step": "2",
                "title": "Explanation",
                "latex": "\\text{The origin } (0, 0) \\text{ has zero distance from the pole, so no unique direction angle exists.}"
            }
        ]

    # Quadrant analysis
    quadrant = ""
    if a > 0 and b >= 0:
        quadrant = "Quadrant I (a > 0, b ≥ 0): θ = arctan(b/a)"
    elif a < 0 and b >= 0:
        quadrant = "Quadrant II (a < 0, b ≥ 0): θ = arctan(b/a) + π"
    elif a < 0 and b < 0:
        quadrant = "Quadrant III (a < 0, b < 0): θ = arctan(b/a) - π"
    elif a > 0 and b < 0:
        quadrant = "Quadrant IV (a > 0, b < 0): θ = arctan(b/a)"
    elif a == 0 and b > 0:
        quadrant = "Positive Imaginary Axis: θ = π/2 (90°)"
    elif a == 0 and b < 0:
        quadrant = "Negative Imaginary Axis: θ = -π/2 (-90°)"

    pi_frac = angle_to_pi_fraction(arg_rad)
    pi_display = f" = {pi_frac}" if pi_frac else ""

    return [
        {
            "step": "1",
            "title": "Identify position and quadrant in the complex plane",
            "latex": f"a = {clean_number(a)}, \\quad b = {clean_number(b)} \\implies \\text{{{quadrant}}}"
        },
        {
            "step": "2",
            "title": "Calculate using the two-argument arctangent function atan2(b, a)",
            "latex": f"\\text{{Arg}}(z) = \\text{{atan2}}({clean_number(b)}, {clean_number(a)})"
        },
        {
            "step": "3",
            "title": "Principal Argument in radians (interval (-π, π])",
            "latex": f"\\theta = {clean_number(arg_rad, 6)}{pi_display}\\text{{ rad}}"
        },
        {
            "step": "4",
            "title": "Convert to degrees",
            "latex": f"\\theta^\\circ = \\theta \\times \\frac{{180^\\circ}}{{\\pi}} = {clean_number(arg_deg, 2)}^\\circ"
        }
    ]


def explain_reciprocal(z: ComplexNum, res: ComplexNum) -> List[Dict[str, str]]:
    mod_sq = z.real**2 + z.imag**2
    z_bar = calc_conj(z)

    return [
        {
            "step": "1",
            "title": "Recall the multiplicative inverse formula",
            "latex": "z^{-1} = \\frac{1}{z} = \\frac{\\overline{z}}{|z|^2} = \\frac{a - bi}{a^2 + b^2}"
        },
        {
            "step": "2",
            "title": "Compute the complex conjugate of z",
            "latex": f"\\overline{{z}} = {z_bar.formatted()}"
        },
        {
            "step": "3",
            "title": "Compute the squared modulus |z|²",
            "latex": f"|z|^2 = ({clean_number(z.real)})^2 + ({clean_number(z.imag)})^2 = {clean_number(mod_sq)}"
        },
        {
            "step": "4",
            "title": "Divide each component by |z|²",
            "latex": f"z^{{-1}} = \\frac{{{z_bar.formatted()}}}{{{clean_number(mod_sq)}}} = {res.formatted()}"
        }
    ]


def explain_powers_of_i(k: int, data: Dict[str, Any]) -> List[Dict[str, str]]:
    q = data["quotient"]
    r = data["remainder"]
    res_str = data["result_str"]

    cycle_exp = {0: "1", 1: "i", 2: "-1", 3: "-i"}[r]

    return [
        {
            "step": "1",
            "title": "Recall the 4-step cyclic pattern of powers of i",
            "latex": "i^0 = 1, \\quad i^1 = i, \\quad i^2 = -1, \\quad i^3 = -i, \\quad i^4 = 1"
        },
        {
            "step": "2",
            "title": "Perform division algorithm with divisor 4",
            "latex": f"{k} = 4 \\times ({q}) + {r}"
        },
        {
            "step": "3",
            "title": "Factor out powers of i⁴ = 1",
            "latex": f"i^{{{k}}} = (i^4)^{{{q}}} \\cdot i^{{{r}}} = (1)^{{{q}}} \\cdot i^{{{r}}}"
        },
        {
            "step": "4",
            "title": "Evaluate the remaining power",
            "latex": f"= 1 \\cdot ({cycle_exp}) = {res_str}"
        }
    ]


def explain_nth_roots(z: ComplexNum, n: int, roots_data: Dict[str, Any]) -> List[Dict[str, str]]:
    r = z.modulus
    theta = z.argument or 0.0
    r_root = roots_data["root_radius"]

    steps = [
        {
            "step": "1",
            "title": "Apply the N-th Roots formula",
            "latex": f"w_k = r^{{1/{n}}} \\left[\\cos\\left(\\frac{{\\theta + 2k\\pi}}{{{n}}}\\right) + i\\sin\\left(\\frac{{\\theta + 2k\\pi}}{{{n}}}\\right)\\right], \\quad k = 0, 1, \\dots, {n-1}"
        },
        {
            "step": "2",
            "title": f"Compute root modulus r^(1/{n})",
            "latex": f"r^{{1/{n}}} = ({clean_number(r, 4)})^{{1/{n}}} \\approx {clean_number(r_root, 6)}"
        }
    ]

    for root in roots_data["roots"][:5]:  # Show up to 5 individual steps
        k = root["k"]
        steps.append({
            "step": f"Root k={k}",
            "title": f"Calculate root for k = {k}",
            "latex": f"w_{{{k}}}: \\text{{Angle }} \\theta_{{{k}}} = {root['angle_rad']}\\text{{ rad}} ({root['angle_deg']}^\\circ) \\implies w_{{{k}}} = {root['formatted']}"
        })

    if n > 5:
        steps.append({
            "step": "Note",
            "title": "Additional roots",
            "latex": f"\\text{{All {n} distinct roots are evenly spaced on a circle of radius {clean_number(r_root, 4)} by }}\\frac{{360^\\circ}}{{{n}}} = {clean_number(360.0/n, 2)}^\\circ."
        })

    return steps


def explain_de_moivre(z: ComplexNum, n: int, data: Dict[str, Any]) -> List[Dict[str, str]]:
    r = data["r"]
    theta = data["theta_rad"]
    r_n = data["r_pow_n"]
    n_theta = data["n_theta_rad"]
    res = data["result"]["formatted"]

    return [
        {
            "step": "1",
            "title": "State De Moivre's Theorem",
            "latex": "[r(\\cos\\theta + i\\sin\\theta)]^n = r^n(\\cos n\\theta + i\\sin n\\theta)"
        },
        {
            "step": "2",
            "title": "Express base z in polar form",
            "latex": f"r = {clean_number(r)}, \\quad \\theta = {clean_number(theta)}\\text{{ rad}}"
        },
        {
            "step": "3",
            "title": "Compute rⁿ and nθ",
            "latex": f"r^{{{n}}} = {clean_number(r)}^{{{n}}} = {clean_number(r_n)}, \\quad n\\theta = {n} \\times ({clean_number(theta)}) = {clean_number(n_theta)}\\text{{ rad}}"
        },
        {
            "step": "4",
            "title": "Convert back to rectangular form",
            "latex": f"z^{{{n}}} = {clean_number(r_n)}(\\cos({clean_number(n_theta)}) + i\\sin({clean_number(n_theta)})) = {res}"
        }
    ]
