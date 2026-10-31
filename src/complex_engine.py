"""ComplexLab Mathematical Calculation Engine
Implements mathematically rigorous operations on complex numbers with exact and numerical representations.
"""
from dataclasses import dataclass
from fractions import Fraction
import cmath
import math
from typing import Optional, Union, List, Tuple, Dict, Any

from src.formatter import format_complex, clean_number, format_polar, format_exponential, format_trigonometric

TOLERANCE = 1e-9


@dataclass
class ComplexNum:
    """Rigorous internal representation of a complex number z = a + bi."""
    real: float
    imag: float

    def __post_init__(self):
        # Clean potential -0.0
        if abs(self.real) < 1e-14:
            self.real = 0.0
        if abs(self.imag) < 1e-14:
            self.imag = 0.0

    @classmethod
    def from_complex(cls, c: complex) -> "ComplexNum":
        return cls(c.real, c.imag)

    @classmethod
    def from_polar(cls, r: float, theta: float) -> "ComplexNum":
        if r < 0:
            raise ValueError("Modulus (r) cannot be negative.")
        real = r * math.cos(theta)
        imag = r * math.sin(theta)
        return cls(real, imag)

    @property
    def is_zero(self) -> bool:
        return abs(self.real) < TOLERANCE and abs(self.imag) < TOLERANCE

    @property
    def modulus(self) -> float:
        """Calculate |z| = sqrt(a^2 + b^2)."""
        return math.hypot(self.real, self.imag)

    @property
    def argument(self) -> Optional[float]:
        """Calculate principal argument arg(z) = atan2(b, a) in (-pi, pi].
        Returns None if z is 0 (argument is undefined).
        """
        if self.is_zero:
            return None
        return math.atan2(self.imag, self.real)

    @property
    def argument_deg(self) -> Optional[float]:
        arg = self.argument
        return math.degrees(arg) if arg is not None else None

    def to_builtin(self) -> complex:
        return complex(self.real, self.imag)

    def formatted(self, precision: int = 6) -> str:
        return format_complex(self.real, self.imag, precision=precision)

    def to_dict(self, precision: int = 6) -> Dict[str, Any]:
        arg_rad = self.argument
        arg_deg = self.argument_deg
        return {
            "real": float(clean_number(self.real, precision)),
            "imaginary": float(clean_number(self.imag, precision)),
            "formatted": self.formatted(precision),
            "modulus": round(self.modulus, precision),
            "argument_radians": round(arg_rad, precision) if arg_rad is not None else None,
            "argument_degrees": round(arg_deg, 2) if arg_deg is not None else None,
            "is_zero": self.is_zero,
            "polar": format_polar(self.modulus, arg_rad, precision=4) if arg_rad is not None else "r = 0 (θ undefined)",
            "exponential": format_exponential(self.modulus, arg_rad, precision=4) if arg_rad is not None else "0",
            "trigonometric": format_trigonometric(self.modulus, arg_rad, precision=4) if arg_rad is not None else "0",
        }


# ==============================================================================
# CATEGORY A: BASIC ARITHMETIC
# ==============================================================================

def add(z1: ComplexNum, z2: ComplexNum) -> ComplexNum:
    """z1 + z2 = (a1 + a2) + (b1 + b2)i"""
    return ComplexNum(z1.real + z2.real, z1.imag + z2.imag)


def subtract(z1: ComplexNum, z2: ComplexNum) -> ComplexNum:
    """z1 - z2 = (a1 - a2) + (b1 - b2)i"""
    return ComplexNum(z1.real - z2.real, z1.imag - z2.imag)


def multiply(z1: ComplexNum, z2: ComplexNum) -> ComplexNum:
    """z1 * z2 = (a1*a2 - b1*b2) + (a1*b2 + a2*b1)i"""
    r = z1.real * z2.real - z1.imag * z2.imag
    i = z1.real * z2.imag + z1.imag * z2.real
    return ComplexNum(r, i)


def divide(z1: ComplexNum, z2: ComplexNum) -> ComplexNum:
    """z1 / z2 = (z1 * conjugate(z2)) / |z2|^2"""
    denom = z2.real ** 2 + z2.imag ** 2
    if denom < 1e-15:
        raise ZeroDivisionError("Cannot divide by zero complex number (denominator has modulus zero).")
    r = (z1.real * z2.real + z1.imag * z2.imag) / denom
    i = (z1.imag * z2.real - z1.real * z2.imag) / denom
    return ComplexNum(r, i)


def negate(z: ComplexNum) -> ComplexNum:
    """-z = -a - bi"""
    return ComplexNum(-z.real, -z.imag)


def equals(z1: ComplexNum, z2: ComplexNum, tol: float = TOLERANCE) -> bool:
    """Check mathematical equality within tolerance: |z1.real - z2.real| < tol and |z1.imag - z2.imag| < tol"""
    return abs(z1.real - z2.real) < tol and abs(z1.imag - z2.imag) < tol


def sum_multiple(z_list: List[ComplexNum]) -> ComplexNum:
    """Calculate sum of multiple complex numbers."""
    if not z_list:
        return ComplexNum(0.0, 0.0)
    total_r = sum(z.real for z in z_list)
    total_i = sum(z.imag for z in z_list)
    return ComplexNum(total_r, total_i)


def product_multiple(z_list: List[ComplexNum]) -> ComplexNum:
    """Calculate product of multiple complex numbers."""
    if not z_list:
        return ComplexNum(1.0, 0.0)
    res = ComplexNum(1.0, 0.0)
    for z in z_list:
        res = multiply(res, z)
    return res


# ==============================================================================
# CATEGORY B: CONJUGATE AND RELATED OPERATIONS
# ==============================================================================

def conjugate(z: ComplexNum) -> ComplexNum:
    """conjugate(a + bi) = a - bi"""
    return ComplexNum(z.real, -z.imag)


def double_conjugate(z: ComplexNum) -> Tuple[ComplexNum, bool]:
    """conjugate(conjugate(z)) = z"""
    conj1 = conjugate(z)
    conj2 = conjugate(conj1)
    is_identity = equals(conj2, z)
    return conj2, is_identity


def real_part(z: ComplexNum) -> float:
    return z.real


def imag_part(z: ComplexNum) -> float:
    return z.imag


def modulus(z: ComplexNum) -> float:
    return z.modulus


def argument(z: ComplexNum) -> Tuple[Optional[float], Optional[float]]:
    """Return principal argument in radians and degrees. None if z == 0."""
    return z.argument, z.argument_deg


def reciprocal(z: ComplexNum) -> ComplexNum:
    """z^(-1) = 1/z = (a - bi) / (a^2 + b^2). Undefined if z == 0."""
    if z.is_zero:
        raise ZeroDivisionError("Multiplicative inverse (reciprocal) is undefined for the zero complex number.")
    return divide(ComplexNum(1.0, 0.0), z)


def verify_conjugate_identities(z: ComplexNum) -> Dict[str, Any]:
    """Verify standard Punjab textbook conjugate identities:
    1. z + z_bar = 2 * Re(z)
    2. z - z_bar = 2i * Im(z)
    3. z * z_bar = |z|^2
    """
    z_bar = conjugate(z)

    # 1. z + z_bar
    sum_val = add(z, z_bar)
    two_re = ComplexNum(2 * z.real, 0.0)
    id1_holds = equals(sum_val, two_re)

    # 2. z - z_bar
    diff_val = subtract(z, z_bar)
    two_i_im = ComplexNum(0.0, 2 * z.imag)
    id2_holds = equals(diff_val, two_i_im)

    # 3. z * z_bar
    prod_val = multiply(z, z_bar)
    mod_sq = z.modulus ** 2
    id3_holds = abs(prod_val.real - mod_sq) < TOLERANCE and abs(prod_val.imag) < TOLERANCE

    return {
        "z": z.to_dict(),
        "conjugate": z_bar.to_dict(),
        "identity_1": {
            "formula": "z + z̄ = 2·Re(z)",
            "lhs": sum_val.formatted(),
            "rhs": two_re.formatted(),
            "holds": id1_holds
        },
        "identity_2": {
            "formula": "z - z̄ = 2i·Im(z)",
            "lhs": diff_val.formatted(),
            "rhs": two_i_im.formatted(),
            "holds": id2_holds
        },
        "identity_3": {
            "formula": "z · z̄ = |z|²",
            "lhs": clean_number(prod_val.real, 6),
            "rhs": clean_number(mod_sq, 6),
            "holds": id3_holds
        }
    }


# ==============================================================================
# CATEGORY C: POLAR & EXPONENTIAL REPRESENTATIONS
# ==============================================================================

def to_polar(z: ComplexNum) -> Dict[str, Any]:
    """Convert rectangular form to polar coordinates (r, theta)."""
    r = z.modulus
    theta = z.argument
    if theta is None:
        return {
            "r": 0.0,
            "theta_radians": None,
            "theta_degrees": None,
            "polar_formatted": "r = 0 (angle undefined)",
            "is_undefined": True
        }
    return {
        "r": r,
        "theta_radians": theta,
        "theta_degrees": math.degrees(theta),
        "polar_formatted": format_polar(r, theta),
        "is_undefined": False
    }


def from_polar(r: float, theta_rad: float) -> ComplexNum:
    """Convert polar coordinates (r, theta in radians) to rectangular form."""
    return ComplexNum.from_polar(r, theta_rad)


def degree_to_radian(degrees: float) -> float:
    return math.radians(degrees)


def radian_to_degree(radians: float) -> float:
    return math.degrees(radians)


# ==============================================================================
# CATEGORY D: POWERS AND ROOTS
# ==============================================================================

def integer_power(z: ComplexNum, n: int) -> ComplexNum:
    """Calculate z^n for integer n (positive, zero, or negative)."""
    if n == 0:
        if z.is_zero:
            # 0^0 convention in complex analysis: usually indeterminate or 1; standard is 1.0
            return ComplexNum(1.0, 0.0)
        return ComplexNum(1.0, 0.0)

    if z.is_zero:
        if n < 0:
            raise ZeroDivisionError("Cannot raise zero to a negative power.")
        return ComplexNum(0.0, 0.0)

    if n < 0:
        pos_power = integer_power(z, -n)
        return reciprocal(pos_power)

    # Use polar form (De Moivre's) for numerical stability and integer exponent
    r = z.modulus
    theta = z.argument
    if theta is None:
        return ComplexNum(0.0, 0.0)

    r_n = r ** n
    theta_n = theta * n
    return ComplexNum(r_n * math.cos(theta_n), r_n * math.sin(theta_n))


def powers_of_i(k: int) -> Dict[str, Any]:
    """Simplify i^k using the 4-cycle:
    i^0 = 1, i^1 = i, i^2 = -1, i^3 = -i.
    """
    rem = k % 4
    cycle_map = {
        0: (ComplexNum(1.0, 0.0), "1"),
        1: (ComplexNum(0.0, 1.0), "i"),
        2: (ComplexNum(-1.0, 0.0), "-1"),
        3: (ComplexNum(0.0, -1.0), "-i"),
    }
    num, rep = cycle_map[rem]
    quotient = k // 4
    return {
        "exponent": k,
        "quotient": quotient,
        "remainder": rem,
        "result_complex": num.to_dict(),
        "result_str": rep,
        "formula": f"i^{{{k}}} = (i^4)^{{{quotient}}} \\cdot i^{{{rem}}} = 1^{{{quotient}}} \\cdot {rep} = {rep}"
    }


def square_roots(z: ComplexNum) -> List[ComplexNum]:
    """Calculate the two distinct square roots of z."""
    if z.is_zero:
        return [ComplexNum(0.0, 0.0)]

    r = z.modulus
    theta = z.argument
    sqrt_r = math.sqrt(r)

    # Root 1 (principal root): k = 0
    w0 = ComplexNum(sqrt_r * math.cos(theta / 2), sqrt_r * math.sin(theta / 2))
    # Root 2: k = 1, exactly -w0
    w1 = negate(w0)
    return [w0, w1]


def nth_roots(z: ComplexNum, n: int) -> List[ComplexNum]:
    """Calculate all n distinct nth roots of z:
    w_k = r^(1/n) * [cos((theta + 2k*pi)/n) + i*sin((theta + 2k*pi)/n)]
    for k = 0, 1, ..., n-1.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Root degree n must be a positive integer greater than or equal to 1.")

    if n > 100:
        raise ValueError("Root degree n exceeds maximum supported value (100).")

    if z.is_zero:
        return [ComplexNum(0.0, 0.0)]

    r = z.modulus
    theta = z.argument
    r_root = r ** (1.0 / n)

    roots = []
    for k in range(n):
        angle = (theta + 2 * math.pi * k) / n
        real = r_root * math.cos(angle)
        imag = r_root * math.sin(angle)
        roots.append(ComplexNum(real, imag))
    return roots


def roots_of_unity(n: int) -> List[ComplexNum]:
    """Calculate the n-th roots of unity (roots of z^n = 1)."""
    return nth_roots(ComplexNum(1.0, 0.0), n)


def complex_power(z1: ComplexNum, z2: ComplexNum) -> ComplexNum:
    """Calculate principal value of z1^z2 = exp(z2 * Ln(z1)).
    Ln(z1) = ln|z1| + i * Arg(z1) for z1 != 0.
    """
    if z1.is_zero:
        if z2.is_zero:
            return ComplexNum(1.0, 0.0)
        if z2.real > 0:
            return ComplexNum(0.0, 0.0)
        raise ZeroDivisionError("Cannot raise zero to a power with non-positive real part.")

    # Using cmath for principal value
    c1 = z1.to_builtin()
    c2 = z2.to_builtin()
    res = c1 ** c2
    return ComplexNum.from_complex(res)


# ==============================================================================
# CATEGORY E: ADVANCED OPERATIONS
# ==============================================================================

def distance(z1: ComplexNum, z2: ComplexNum) -> float:
    """d(z1, z2) = |z1 - z2|"""
    diff = subtract(z1, z2)
    return diff.modulus


def normalize(z: ComplexNum) -> ComplexNum:
    """Normalize nonzero complex number to unit circle: z / |z|"""
    if z.is_zero:
        raise ZeroDivisionError("Cannot normalize the zero complex number (magnitude is zero).")
    mod = z.modulus
    return ComplexNum(z.real / mod, z.imag / mod)


def verify_multiplicative_inverse(z: ComplexNum) -> Dict[str, Any]:
    """Find z^(-1) and verify z * z^(-1) = 1."""
    if z.is_zero:
        raise ZeroDivisionError("Zero has no multiplicative inverse.")
    inv = reciprocal(z)
    prod = multiply(z, inv)
    is_identity = equals(prod, ComplexNum(1.0, 0.0))
    return {
        "z": z.to_dict(),
        "inverse": inv.to_dict(),
        "product": prod.to_dict(),
        "verified": is_identity,
        "formula": "z \\cdot z^{-1} = 1"
    }


def product_with_conjugate(z: ComplexNum) -> Dict[str, Any]:
    """z * conjugate(z) = |z|^2"""
    z_bar = conjugate(z)
    prod = multiply(z, z_bar)
    mod_sq = z.modulus ** 2
    return {
        "z": z.to_dict(),
        "conjugate": z_bar.to_dict(),
        "product": prod.to_dict(),
        "modulus_squared": mod_sq,
        "is_real": abs(prod.imag) < TOLERANCE
    }
