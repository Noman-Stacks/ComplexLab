"""ComplexLab Formatter Module
Handles mathematical formatting of complex numbers, real values, polar forms, and LaTeX output.
"""
from fractions import Fraction
import math

TOLERANCE = 1e-9


def clean_number(val, precision=6):
    """Format a real or float number cleanly:
    - Avoids -0 or -0.0
    - If it's an integer or within tolerance of an integer, formats as integer
    - Strips unnecessary trailing zeroes after decimal point
    """
    if val is None:
        return "0"
    if isinstance(val, (int, Fraction)):
        if isinstance(val, Fraction) and val.denominator == 1:
            return str(val.numerator)
        return str(val)

    # Float handling
    if abs(val) < 1e-12:
        return "0"

    # Check if close to integer
    rounded_int = round(val)
    if abs(val - rounded_int) < 1e-9:
        if rounded_int == 0:
            return "0"
        return str(rounded_int)

    # Format with precision
    s = f"{val:.{precision}f}".rstrip("0").rstrip(".")
    if s == "-0" or s == "":
        return "0"
    return s


def format_complex(real, imag, precision=6, use_latex=False):
    """Format a complex number z = real + imag*i.
    Rules:
    - 0 + 0i -> 0
    - 3 + 0i -> 3
    - 0 + 4i -> 4i
    - 0 - 4i -> -4i
    - 0 + 1i -> i
    - 0 - 1i -> -i
    - 3 + 1i -> 3 + i
    - 3 - 1i -> 3 - i
    - 3 + 4i -> 3 + 4i
    - 3 - 4i -> 3 - 4i
    - Never displays -0 or 3 + -4i
    """
    # Clean zero check
    if abs(real) < 1e-12:
        real = 0.0 if not isinstance(real, (int, Fraction)) else 0
    if abs(imag) < 1e-12:
        imag = 0.0 if not isinstance(imag, (int, Fraction)) else 0

    is_real_zero = (abs(real) < 1e-12) if isinstance(real, float) else (real == 0)
    is_imag_zero = (abs(imag) < 1e-12) if isinstance(imag, float) else (imag == 0)

    if is_real_zero and is_imag_zero:
        return "0"

    if is_imag_zero:
        return clean_number(real, precision)

    # Format imaginary coefficient
    abs_imag = abs(imag)
    is_imag_one = (abs(abs_imag - 1.0) < 1e-12) if isinstance(abs_imag, float) else (abs_imag == 1)

    imag_sign = "-" if (imag < -1e-12) else ("+" if not is_real_zero else "")

    if is_imag_one:
        imag_str = "i"
    else:
        imag_str = f"{clean_number(abs_imag, precision)}i"

    if is_real_zero:
        if imag_sign == "-":
            return f"-{imag_str}"
        return imag_str

    real_str = clean_number(real, precision)
    return f"{real_str} {imag_sign} {imag_str}"


def format_latex_complex(real, imag, precision=6):
    """Format a complex number as LaTeX."""
    plain = format_complex(real, imag, precision, use_latex=True)
    # If it's a fraction or complex, wrap if necessary
    return plain


def angle_to_pi_fraction(theta, tolerance=1e-3):
    """Recognize standard angle multiples of pi (e.g. pi/6, pi/4, pi/3, pi/2, pi, etc.)."""
    if abs(theta) < tolerance:
        return "0"

    ratio = theta / math.pi
    # Try small denominators up to 12
    for denom in [1, 2, 3, 4, 6, 8, 12]:
        num = round(ratio * denom)
        if abs(ratio - num / denom) < tolerance:
            if num == 0:
                return "0"
            if denom == 1:
                return r"\pi" if num == 1 else (r"-\pi" if num == -1 else f"{num}\\pi")
            sign = "-" if num < 0 else ""
            abs_num = abs(num)
            if abs_num == 1:
                return f"{sign}\\frac{{\\pi}}{{{denom}}}"
            return f"{sign}\\frac{{{abs_num}\\pi}}{{{denom}}}"
    return None


def format_polar(r, theta, precision=4, use_latex=False):
    """Format polar representation (r, theta)."""
    r_str = clean_number(r, precision)
    theta_rad_str = clean_number(theta, precision)
    deg = math.degrees(theta)
    deg_str = clean_number(deg, 2)
    pi_frac = angle_to_pi_fraction(theta)

    if use_latex:
        theta_latex = f"\\approx {theta_rad_str}\\text{{ rad}}" if not pi_frac else f"{pi_frac} \\approx {theta_rad_str}\\text{{ rad}}"
        return f"({r_str}, {theta_latex})"

    return f"r = {r_str}, θ = {theta_rad_str} rad ({deg_str}°)"


def format_exponential(r, theta, precision=4, use_latex=False):
    """Format exponential representation: r * e^(i*theta)."""
    r_str = clean_number(r, precision)
    theta_str = clean_number(theta, precision)
    pi_frac = angle_to_pi_fraction(theta)

    if use_latex:
        exp_arg = pi_frac if pi_frac else theta_str
        if r_str == "1":
            return f"e^{{i({exp_arg})}}"
        return f"{r_str} e^{{i({exp_arg})}}"

    if r_str == "1":
        return f"e^(i * {theta_str})"
    return f"{r_str} * e^(i * {theta_str})"


def format_trigonometric(r, theta, precision=4, use_latex=False):
    """Format trigonometric form: r*(cos(theta) + i*sin(theta))."""
    r_str = clean_number(r, precision)
    theta_str = clean_number(theta, precision)
    pi_frac = angle_to_pi_fraction(theta)
    angle_display = pi_frac if (use_latex and pi_frac) else theta_str

    if use_latex:
        if r_str == "1":
            return f"\\cos({angle_display}) + i\\sin({angle_display})"
        return f"{r_str}\\left(\\cos({angle_display}) + i\\sin({angle_display})\\right)"

    if r_str == "1":
        return f"cos({theta_str}) + i*sin({theta_str})"
    return f"{r_str}*(cos({theta_str}) + i*sin({theta_str}))"
