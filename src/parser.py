"""ComplexLab Safe Mathematical Expression Parser
Safely parses complex numbers and arithmetic expressions without eval().
Supports rectangular inputs and algebraic expressions with i or j.
"""
import ast
import math
import re
from fractions import Fraction

MAX_INPUT_LENGTH = 200
MAX_EXPONENT = 1000


class ParseError(ValueError):
    """Custom exception for parsing errors with user-friendly messages."""
    pass


def sanitize_input(expr_str: str) -> str:
    """Preprocess and sanitize mathematical input string for parsing."""
    if not isinstance(expr_str, str):
        raise ParseError("Input must be a string.")

    s = expr_str.strip()
    if not s:
        raise ParseError("Input expression cannot be empty.")

    if len(s) > MAX_INPUT_LENGTH:
        raise ParseError(f"Input is too long (maximum {MAX_INPUT_LENGTH} characters).")

    # Reject dangerous keywords or characters
    forbidden = ["__", "import", "exec", "eval", "lambda", "class", "def", "open", "os", "sys"]
    for word in forbidden:
        if word in s.lower():
            raise ParseError(f"Invalid keyword or syntax: '{word}'")

    # Replace unicode minus, multiplication, division symbols
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/")
    s = s.replace("·", "*").replace("π", "pi")

    # Support fraction coefficients for i: e.g. '3/4i' -> '((3/4)*i)'
    s = re.sub(r"(\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?)\s*([ijIJ])\b", r"((\1)*\2)", s)

    # Support implicit multiplication before i or j: e.g. '3i' -> '3*i', '4.5j' -> '4.5*j'
    # Pattern: digit or decimal followed by i or j
    s = re.sub(r"(\d+(\.\d+)?)\s*([ijIJ])\b", r"(\1*\3)", s)

    # Support standalone i or j: e.g. "+i", "-i", "(i)", " i " -> replaced with 1*i
    # At start of expression:
    s = re.sub(r"^\s*([ijIJ])\b", r"(1*\1)", s)
    # After operator or parenthesis:
    s = re.sub(r"([+\-*/(])\s*([ijIJ])\b", r"\1(1*\2)", s)

    # Implicit multiplication between closing paren and opening paren or number or i
    s = re.sub(r"\)\s*\(", ")*(", s)
    s = re.sub(r"(\d+(\.\d+)?)\s*\(", r"\1*(", s)
    s = re.sub(r"\)\s*(\d+(\.\d+)?)", r")*\1", s)
    s = re.sub(r"\)\s*([ijIJ])\b", r")*\1", s)

    # Normalize I/J to I
    s = re.sub(r"\b[ijIJ]\b", "I", s)

    return s


def _eval_ast_node(node):
    """Recursively and safely evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)

    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, complex)):
            return complex(node.value)
        raise ParseError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.Name):
        if node.id == "I":
            return complex(0, 1)
        elif node.id == "pi":
            return complex(math.pi, 0)
        elif node.id == "e":
            return complex(math.e, 0)
        raise ParseError(f"Unknown variable or identifier: '{node.id}'. Only 'i' or 'j' is supported.")

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        raise ParseError(f"Unsupported unary operator: {type(node.op).__name__}")

    elif isinstance(node, ast.BinOp):
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if abs(right) < 1e-15:
                raise ParseError("Division by zero in expression.")
            return left / right
        elif isinstance(node.op, ast.Pow):
            # Guard against huge exponents
            if abs(right.imag) > 1e-12:
                # Complex exponent
                return left ** right
            if abs(right.real) > MAX_EXPONENT:
                raise ParseError(f"Exponent exceeds maximum allowed magnitude ({MAX_EXPONENT}).")
            return left ** right
        raise ParseError(f"Unsupported binary operator: {type(node.op).__name__}")

    raise ParseError(f"Unsupported expression syntax: {type(node).__name__}")


def parse_complex_expression(expr_str: str) -> complex:
    """Safely parse a complex expression string into a Python complex number without eval().
    Supports forms like:
    '3 + 4i', '3-4i', '-2+5i', '7i', '-7i', '5', '-3', 'i', '-i', '0', '0+0i',
    '1.5 + 2.75i', '(2-3i)*(1+i)', '1/2 + 3/4i', etc.
    """
    sanitized = sanitize_input(expr_str)

    try:
        parsed_tree = ast.parse(sanitized, mode="eval")
    except SyntaxError as e:
        raise ParseError(f"Invalid mathematical syntax: '{expr_str}'. Please check parentheses and operators.") from e

    res = _eval_ast_node(parsed_tree)

    # Clean tiny numerical noise around zero
    real = res.real if abs(res.real) > 1e-14 else 0.0
    imag = res.imag if abs(res.imag) > 1e-14 else 0.0
    return complex(real, imag)


def parse_rectangular_inputs(real_val, imag_val) -> complex:
    """Parse separate real and imaginary inputs (Mode A).
    Accepts numbers, strings with numbers/fractions, or None.
    """
    def _parse_part(val, name):
        if val is None or val == "":
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip()
        if not val_str:
            return 0.0
        # Check fraction like '1/2' or '-3/4'
        if "/" in val_str:
            parts = val_str.split("/")
            if len(parts) == 2:
                try:
                    num = float(parts[0].strip())
                    den = float(parts[1].strip())
                    if abs(den) < 1e-15:
                        raise ParseError(f"Denominator cannot be zero in {name} part: '{val_str}'")
                    return num / den
                except ValueError:
                    pass
        try:
            return float(val_str)
        except ValueError:
            raise ParseError(f"Invalid numeric value for {name} part: '{val_str}'")

    real = _parse_part(real_val, "real")
    imag = _parse_part(imag_val, "imaginary")
    return complex(real, imag)


def parse_number_list(numbers_str: str) -> list[complex]:
    """Parse comma or semicolon separated list of complex expressions."""
    if not numbers_str or not numbers_str.strip():
        raise ParseError("Numbers list cannot be empty.")

    tokens = [t.strip() for t in re.split(r"[,;]+", numbers_str.strip()) if t.strip()]
    if not tokens:
        raise ParseError("No valid numbers found in input list.")

    return [parse_complex_expression(t) for t in tokens]
