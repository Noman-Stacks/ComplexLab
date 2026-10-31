"""ComplexLab Practice and Exercise Module
Generates mathematically verified questions with multiple choice and free input,
provides hints, detailed step-by-step solutions, and verifies user answers using numeric tolerance.
"""
import random
import math
import uuid
from typing import Dict, Any, List, Optional
from src.complex_engine import (
    ComplexNum, add, subtract, multiply, divide, conjugate, modulus, powers_of_i
)
from src.parser import parse_complex_expression, ParseError
from src.formatter import clean_number, format_complex

TOPICS = ["arithmetic", "conjugate_modulus", "polar_exponential", "powers_roots", "equations"]
DIFFICULTIES = ["beginner", "intermediate", "advanced"]


def _random_complex(min_val=-5, max_val=5, nonzero=True) -> ComplexNum:
    """Generate a random complex number with integer parts."""
    while True:
        r = random.randint(min_val, max_val)
        i = random.randint(min_val, max_val)
        if nonzero and (r == 0 and i == 0):
            continue
        return ComplexNum(float(r), float(i))


def _build_solution_text(steps: List[Dict[str, str]], final_ans: str) -> str:
    """Construct readable multi-line plaintext solution from steps list."""
    lines = []
    for s in steps:
        step_num = s.get("step", "")
        title = s.get("title", "")
        desc = s.get("description", "")
        latex = s.get("latex", "")
        lines.append(f"Step {step_num}: {title}")
        if desc:
            lines.append(f"  {desc}")
        if latex:
            lines.append(f"  {latex}")
        lines.append("")
    lines.append(f"Final Answer: {final_ans}")
    return "\n".join(lines)


def generate_arithmetic_question(difficulty: str) -> Dict[str, Any]:
    """Generate addition, subtraction, multiplication, or division question with complete steps."""
    ops = ["+", "-", "*"]
    if difficulty in ["intermediate", "advanced"]:
        ops.append("/")

    op = random.choice(ops)
    range_lim = 5 if difficulty == "beginner" else (8 if difficulty == "intermediate" else 12)
    z1 = _random_complex(-range_lim, range_lim)
    z2 = _random_complex(-range_lim, range_lim, nonzero=True)

    steps = []

    if op == "+":
        res = add(z1, z2)
        question_text = f"Calculate the sum: $({z1.formatted()}) + ({z2.formatted()})$"
        hint = "Add the real parts together, and add the imaginary parts together."
        steps = [
            {
                "step": "1",
                "title": "State the addition expression",
                "description": "Write out the two complex numbers to be added in standard form:",
                "latex": f"z_1 + z_2 = ({z1.formatted()}) + ({z2.formatted()})"
            },
            {
                "step": "2",
                "title": "Group real and imaginary components",
                "description": "Combine the real components together, and group the imaginary components together:",
                "latex": f"= [{clean_number(z1.real)} + ({clean_number(z2.real)})] + [{clean_number(z1.imag)} + ({clean_number(z2.imag)})]i"
            },
            {
                "step": "3",
                "title": "Perform the additions",
                "description": "Compute the sums inside each bracket:",
                "latex": f"= {clean_number(res.real)} + ({clean_number(res.imag)})i"
            },
            {
                "step": "4",
                "title": "Write final standard form",
                "description": "Combine into standard complex representation $a + bi$:",
                "latex": f"z_1 + z_2 = {res.formatted()}"
            }
        ]

    elif op == "-":
        res = subtract(z1, z2)
        question_text = f"Calculate the difference: $({z1.formatted()}) - ({z2.formatted()})$"
        hint = "Subtract real parts and subtract imaginary parts. Remember to distribute the minus sign!"
        steps = [
            {
                "step": "1",
                "title": "State the subtraction expression",
                "description": "Set up the subtraction of the second complex number from the first:",
                "latex": f"z_1 - z_2 = ({z1.formatted()}) - ({z2.formatted()})"
            },
            {
                "step": "2",
                "title": "Distribute the negative sign across z₂",
                "description": "Multiply each term inside the second parenthesis by -1:",
                "latex": f"= ({z1.formatted()}) + [{-z2.real:+g} {-z2.imag:+g}i]".replace("+-", "-")
            },
            {
                "step": "3",
                "title": "Group real and imaginary parts",
                "description": "Collect the real numbers and the imaginary coefficients:",
                "latex": f"= [{clean_number(z1.real)} - ({clean_number(z2.real)})] + [{clean_number(z1.imag)} - ({clean_number(z2.imag)})]i"
            },
            {
                "step": "4",
                "title": "Simplify and state final result",
                "description": "Evaluate the subtractions to obtain the final complex number:",
                "latex": f"z_1 - z_2 = {res.formatted()}"
            }
        ]

    elif op == "*":
        res = multiply(z1, z2)
        question_text = f"Calculate the product: $({z1.formatted()}) \\times ({z2.formatted()})$"
        hint = "Use the distributive property (FOIL) and remember the fundamental identity $i^2 = -1$."
        ac = z1.real * z2.real
        ad = z1.real * z2.imag
        bc = z1.imag * z2.real
        bd = z1.imag * z2.imag
        steps = [
            {
                "step": "1",
                "title": "Write the binomial product",
                "description": "Set up the product of the two complex numbers:",
                "latex": f"({z1.formatted()}) \\times ({z2.formatted()})"
            },
            {
                "step": "2",
                "title": "Apply distributive property (FOIL)",
                "description": "Multiply every term in the first number by every term in the second number:",
                "latex": f"= ({clean_number(z1.real)} \\cdot {clean_number(z2.real)}) + ({clean_number(z1.real)} \\cdot {clean_number(z2.imag)}i) + ({clean_number(z1.imag)}i \\cdot {clean_number(z2.real)}) + ({clean_number(z1.imag)}i \\cdot {clean_number(z2.imag)}i)"
            },
            {
                "step": "3",
                "title": "Multiply individual terms",
                "description": "Compute each product and identify the $i^2$ term:",
                "latex": f"= {clean_number(ac)} + ({clean_number(ad)}i) + ({clean_number(bc)}i) + ({clean_number(bd)}i^2)"
            },
            {
                "step": "4",
                "title": "Substitute i² = -1",
                "description": "Since $i^2 = -1$, the term with $i^2$ becomes a real number:",
                "latex": f"= {clean_number(ac)} + {clean_number(ad + bc)}i + {clean_number(bd)}(-1) = {clean_number(ac)} - {clean_number(bd)} + {clean_number(ad + bc)}i"
            },
            {
                "step": "5",
                "title": "Combine real and imaginary parts",
                "description": "Group real terms $(ac - bd)$ and imaginary terms $(ad + bc)i$:",
                "latex": f"= {res.formatted()}"
            }
        ]

    else:  # division
        nice_denoms = [ComplexNum(1, 1), ComplexNum(1, -1), ComplexNum(2, 1), ComplexNum(1, 2), ComplexNum(3, 4)]
        z2 = random.choice(nice_denoms)
        res = divide(z1, z2)
        z2_bar = conjugate(z2)
        denom_val = z2.real**2 + z2.imag**2
        num_prod = multiply(z1, z2_bar)

        question_text = f"Calculate the quotient: $\\frac{{{z1.formatted()}}}{{{z2.formatted()}}}$"
        hint = "Multiply both numerator and denominator by the complex conjugate of the denominator."
        steps = [
            {
                "step": "1",
                "title": "Write the expression as a fraction",
                "description": "Set up the quotient of $z_1$ divided by $z_2$:",
                "latex": f"\\frac{{z_1}}{{z_2}} = \\frac{{{z1.formatted()}}}{{{z2.formatted()}}}"
            },
            {
                "step": "2",
                "title": "Find the complex conjugate of the denominator",
                "description": "Invert the sign of the imaginary component of $z_2$:",
                "latex": f"\\overline{{z_2}} = \\overline{{{z2.formatted()}}} = {z2_bar.formatted()}"
            },
            {
                "step": "3",
                "title": "Multiply numerator and denominator by the conjugate",
                "description": "This realizes the denominator by turning it into a real number:",
                "latex": f"= \\frac{{({z1.formatted()})({z2_bar.formatted()})}}{{({z2.formatted()})({z2_bar.formatted()})}}"
            },
            {
                "step": "4",
                "title": "Simplify the denominator using z · z̄ = a² + b²",
                "description": "Evaluate the real denominator:",
                "latex": f"\\text{{Denominator: }} ({clean_number(z2.real)})^2 + ({clean_number(z2.imag)})^2 = {clean_number(denom_val)}"
            },
            {
                "step": "5",
                "title": "Expand the numerator",
                "description": "Multiply out $(z_1)(\\bar{z_2})$:",
                "latex": f"\\text{{Numerator: }} ({z1.formatted()})({z2_bar.formatted()}) = {num_prod.formatted()}"
            },
            {
                "step": "6",
                "title": "Divide each term by the real denominator",
                "description": "Separate into standard form $a + bi$:",
                "latex": f"= \\frac{{{clean_number(num_prod.real)}}}{{{clean_number(denom_val)}}} + \\frac{{{clean_number(num_prod.imag)}}}{{{clean_number(denom_val)}}}i = {res.formatted()}"
            }
        ]

    q_type = "multiple_choice" if random.random() < 0.6 else "free_input"

    options = []
    if q_type == "multiple_choice":
        correct_str = res.formatted()
        distractors = {
            correct_str,
            format_complex(-res.real, res.imag),
            format_complex(res.real, -res.imag),
            format_complex(res.imag, res.real),
            format_complex(res.real + 1, res.imag),
            format_complex(res.real, res.imag - 1)
        }
        distractors.discard(correct_str)
        options = [correct_str] + list(distractors)[:3]
        random.shuffle(options)

    solution_text = _build_solution_text(steps, res.formatted())

    return {
        "id": str(uuid.uuid4())[:8],
        "topic": "arithmetic",
        "difficulty": difficulty,
        "type": q_type,
        "question": question_text,
        "options": options,
        "correct_answer": res.formatted(),
        "correct_real": res.real,
        "correct_imag": res.imag,
        "is_complex": True,
        "hint": hint,
        "solution": solution_text,
        "steps": steps
    }


def generate_conjugate_modulus_question(difficulty: str) -> Dict[str, Any]:
    """Generate question about conjugate, real part, imaginary part, or modulus with complete steps."""
    q_choice = random.choice(["conjugate", "modulus", "parts", "identity"])
    z = _random_complex(-6, 6)
    steps = []

    if q_choice == "conjugate":
        res = conjugate(z)
        question_text = f"Find the complex conjugate of $z = {z.formatted()}$."
        hint = "To find the conjugate z̄ of a + bi, invert the sign of the imaginary part: z̄ = a - bi."
        steps = [
            {
                "step": "1",
                "title": "Recall the definition of complex conjugate",
                "description": "The complex conjugate of $z = a + bi$, denoted $\\bar{z}$, is obtained by changing the sign of the imaginary part:",
                "latex": "\\overline{a + bi} = a - bi"
            },
            {
                "step": "2",
                "title": "Identify components of z",
                "description": "Extract the real and imaginary parts from the given complex number:",
                "latex": f"a = \\text{{Re}}(z) = {clean_number(z.real)}, \\quad b = \\text{{Im}}(z) = {clean_number(z.imag)}"
            },
            {
                "step": "3",
                "title": "Invert the sign of the imaginary component",
                "description": "Keep the real part unchanged and negate $b$:",
                "latex": f"b \\to -({clean_number(z.imag)}) = {clean_number(-z.imag)}"
            },
            {
                "step": "4",
                "title": "State the final conjugate",
                "description": "Combine the real part and the negated imaginary part:",
                "latex": f"\\overline{{z}} = {res.formatted()}"
            }
        ]
        correct_answer = res.formatted()
        correct_real = res.real
        correct_imag = res.imag
        is_complex = True

    elif q_choice == "modulus":
        triples = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (5, 12, 13)]
        if difficulty in ["beginner", "intermediate"]:
            a_val, b_val, mod_val = random.choice(triples)
            sa = random.choice([1, -1])
            sb = random.choice([1, -1])
            z = ComplexNum(sa * a_val, sb * b_val)
            ans = float(mod_val)
        else:
            ans = z.modulus

        a_sq = z.real ** 2
        b_sq = z.imag ** 2
        sum_sq = a_sq + b_sq

        question_text = f"Calculate the modulus (absolute value) $|z|$ for $z = {z.formatted()}$."
        hint = "Use the modulus formula: $|z| = \\sqrt{a^2 + b^2}$."
        steps = [
            {
                "step": "1",
                "title": "Recall the modulus formula",
                "description": "The modulus $|z|$ of a complex number $z = a + bi$ represents its Euclidean distance from the origin on the complex plane:",
                "latex": "|z| = \\sqrt{a^2 + b^2}"
            },
            {
                "step": "2",
                "title": "Identify real part a and imaginary part b",
                "description": "Extract the components from $z$:",
                "latex": f"a = \\text{{Re}}(z) = {clean_number(z.real)}, \\quad b = \\text{{Im}}(z) = {clean_number(z.imag)}"
            },
            {
                "step": "3",
                "title": "Substitute the components into the radical",
                "description": "Square both $a$ and $b$ and sum them:",
                "latex": f"|z| = \\sqrt{{({clean_number(z.real)})^2 + ({clean_number(z.imag)})^2}} = \\sqrt{{{clean_number(a_sq)} + {clean_number(b_sq)}}}"
            },
            {
                "step": "4",
                "title": "Sum the squared components",
                "description": "Add the squares inside the square root:",
                "latex": f"= \\sqrt{{{clean_number(sum_sq)}}}"
            },
            {
                "step": "5",
                "title": "Evaluate the principal square root",
                "description": "Since the distance $|z| \\ge 0$, calculate the non-negative square root:",
                "latex": f"|z| = {clean_number(ans, 4)}"
            }
        ]
        correct_answer = clean_number(ans, 4)
        correct_real = ans
        correct_imag = 0.0
        is_complex = False

    elif q_choice == "parts":
        part = random.choice(["Re", "Im"])
        if part == "Re":
            ans = z.real
            question_text = f"Identify the real part $\\text{{Re}}(z)$ for $z = {z.formatted()}$."
            hint = "In standard form z = a + bi, the real part is a."
            steps = [
                {
                    "step": "1",
                    "title": "Recall standard complex representation",
                    "description": "Any complex number is written as $z = a + bi$, where $a$ and $b$ are real numbers.",
                    "latex": "z = a + bi \\implies \\text{Re}(z) = a, \\quad \\text{Im}(z) = b"
                },
                {
                    "step": "2",
                    "title": "Compare with the given number",
                    "description": f"For $z = {z.formatted()}$, identify the term without $i$:",
                    "latex": f"a = \\text{{Re}}(z) = {clean_number(ans)}"
                },
                {
                    "step": "3",
                    "title": "Conclude the real part",
                    "description": "The real part is strictly a real scalar:",
                    "latex": f"\\text{{Re}}(z) = {clean_number(ans)}"
                }
            ]
        else:
            ans = z.imag
            question_text = f"Identify the imaginary part $\\text{{Im}}(z)$ for $z = {z.formatted()}$."
            hint = "In standard form z = a + bi, the imaginary part is the real coefficient b multiplying i."
            steps = [
                {
                    "step": "1",
                    "title": "Recall definition of imaginary part",
                    "description": "For $z = a + bi$, the imaginary part $\\text{Im}(z)$ is the real scalar coefficient $b$ that multiplies the imaginary unit $i$ (it does NOT include $i$ itself).",
                    "latex": "\\text{Im}(a + bi) = b \\in \\mathbb{R}"
                },
                {
                    "step": "2",
                    "title": "Extract the coefficient of i",
                    "description": f"In the given number $z = {z.formatted()}$, examine the coefficient multiplying $i$:",
                    "latex": f"b = \\text{{Im}}(z) = {clean_number(ans)}"
                },
                {
                    "step": "3",
                    "title": "Conclude the imaginary part",
                    "description": "State the final real scalar value:",
                    "latex": f"\\text{{Im}}(z) = {clean_number(ans)}"
                }
            ]
        correct_answer = clean_number(ans)
        correct_real = ans
        correct_imag = 0.0
        is_complex = False

    else:  # identity
        ans_val = z.modulus ** 2
        ans = clean_number(ans_val, 4)
        z_bar = conjugate(z)
        question_text = f"Evaluate the product of $z$ and its conjugate $z \\bar{{z}}$ for $z = {z.formatted()}$."
        hint = "Recall the fundamental identity $z \\cdot \\bar{z} = |z|^2 = a^2 + b^2$."
        steps = [
            {
                "step": "1",
                "title": "Recall the conjugate product identity",
                "description": "The product of any complex number $z = a + bi$ with its conjugate $\\bar{z} = a - bi$ is always a non-negative real number equal to $|z|^2$:",
                "latex": "z \\cdot \\overline{z} = (a + bi)(a - bi) = a^2 + b^2 = |z|^2"
            },
            {
                "step": "2",
                "title": "Find the conjugate of z",
                "description": f"Given $z = {z.formatted()}$, invert the imaginary sign:",
                "latex": f"\\overline{{z}} = {z_bar.formatted()}"
            },
            {
                "step": "3",
                "title": "Expand the product algebraically",
                "description": "Multiply $(z)(\\bar{z})$ using FOIL and $i^2 = -1$:",
                "latex": f"({z.formatted()})({z_bar.formatted()}) = ({clean_number(z.real)})^2 - ({clean_number(z.imag)}i)^2 = ({clean_number(z.real)})^2 + ({clean_number(z.imag)})^2"
            },
            {
                "step": "4",
                "title": "Calculate the sum of squares",
                "description": "Compute the numerical value:",
                "latex": f"= {clean_number(z.real**2)} + {clean_number(z.imag**2)} = {ans}"
            }
        ]
        correct_answer = ans
        correct_real = float(ans)
        correct_imag = 0.0
        is_complex = False

    q_type = "multiple_choice" if random.random() < 0.6 else "free_input"
    options = []
    if q_type == "multiple_choice":
        if is_complex:
            distractors = {
                correct_answer,
                format_complex(correct_real, -correct_imag),
                format_complex(-correct_real, correct_imag),
                format_complex(correct_imag, correct_real)
            }
        else:
            distractors = {
                correct_answer,
                clean_number(correct_real + 2),
                clean_number(correct_real - 2),
                clean_number(abs(correct_real) + 5)
            }
        distractors.discard(correct_answer)
        options = [correct_answer] + list(distractors)[:3]
        random.shuffle(options)

    solution_text = _build_solution_text(steps, correct_answer)

    return {
        "id": str(uuid.uuid4())[:8],
        "topic": "conjugate_modulus",
        "difficulty": difficulty,
        "type": q_type,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "correct_real": correct_real,
        "correct_imag": correct_imag,
        "is_complex": is_complex,
        "hint": hint,
        "solution": solution_text,
        "steps": steps
    }


def generate_powers_roots_question(difficulty: str) -> Dict[str, Any]:
    """Generate powers of i, square roots, or De Moivre questions with complete steps."""
    q_type_choice = random.choice(["power_i", "square_root", "de_moivre"])
    steps = []

    if q_type_choice == "power_i":
        k = random.randint(5, 120) if difficulty != "beginner" else random.randint(4, 25)
        pow_info = powers_of_i(k)
        ans = pow_info["result_str"]
        q = pow_info["quotient"]
        r = pow_info["remainder"]
        res_complex = pow_info["result_complex"]

        question_text = f"Simplify the power of the imaginary unit: $i^{{{k}}}$."
        hint = "Divide the exponent by 4 and check the remainder: i⁴ = 1."

        cycle_name = {0: "1", 1: "i", 2: "-1", 3: "-i"}[r]
        steps = [
            {
                "step": "1",
                "title": "Recall the 4-step cyclic pattern of powers of i",
                "description": "Powers of $i$ repeat every 4 steps because $i^4 = (i^2)^2 = (-1)^2 = 1$:",
                "latex": "i^0 = 1, \\quad i^1 = i, \\quad i^2 = -1, \\quad i^3 = -i, \\quad i^4 = 1"
            },
            {
                "step": "2",
                "title": "Apply Euclidean division algorithm to the exponent",
                "description": f"Divide exponent {k} by 4 to determine the quotient and remainder:",
                "latex": f"{k} = 4 \\times {q} + {r} \\implies \\text{{Quotient }} q = {q}, \\quad \\text{{Remainder }} r = {r}"
            },
            {
                "step": "3",
                "title": "Decompose the power using exponent rules",
                "description": "Separate the multiple of 4 from the remainder:",
                "latex": f"i^{{{k}}} = i^{{4 \\times {q} + {r}}} = (i^4)^{{{q}}} \\cdot i^{{{r}}} = (1)^{{{q}}} \\cdot i^{{{r}}}"
            },
            {
                "step": "4",
                "title": "Evaluate the simplified power",
                "description": f"Since $1^{{{q}}} = 1$, evaluate $i^{{{r}}}$:",
                "latex": f"i^{{{k}}} = 1 \\cdot ({cycle_name}) = {ans}"
            }
        ]
        options = ["1", "-1", "i", "-i"]
        solution_text = _build_solution_text(steps, ans)

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "powers_roots",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": ans,
            "correct_real": res_complex["real"],
            "correct_imag": res_complex["imaginary"],
            "is_complex": True,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }

    elif q_type_choice == "square_root":
        base = random.choice([ComplexNum(2, 1), ComplexNum(1, 2), ComplexNum(3, 2), ComplexNum(2, -1)])
        z = multiply(base, base)
        question_text = f"Find a square root of $z = {z.formatted()}$."
        hint = "Square each candidate option or use polar half-angle formula."

        steps = [
            {
                "step": "1",
                "title": "State the square root definition",
                "description": "A square root of $z$ is any complex number $w = x + yi$ satisfying $w^2 = z$:",
                "latex": "w^2 = (x + yi)^2 = x^2 - y^2 + 2xyi = z"
            },
            {
                "step": "2",
                "title": "Equate real and imaginary parts",
                "description": f"For $z = {z.formatted()}$, set up the system of equations:",
                "latex": f"x^2 - y^2 = {clean_number(z.real)}, \\quad 2xy = {clean_number(z.imag)}"
            },
            {
                "step": "3",
                "title": "Compute the modulus equation",
                "description": "Use $|w|^2 = |z| = \\sqrt{a^2 + b^2}$:",
                "latex": f"x^2 + y^2 = |{z.formatted()}| = \\sqrt{{({clean_number(z.real)})^2 + ({clean_number(z.imag)})^2}} = {clean_number(base.modulus**2)}"
            },
            {
                "step": "4",
                "title": "Solve for x and y",
                "description": "Add and subtract the equations to solve for $x$ and $y$:",
                "latex": f"2x^2 = {clean_number(z.real + base.modulus**2)} \\implies x = \\pm {clean_number(abs(base.real))}, \\quad y = \\pm {clean_number(abs(base.imag))}"
            },
            {
                "step": "5",
                "title": "State the two square roots",
                "description": f"Matching signs with $2xy = {clean_number(z.imag)}$:",
                "latex": f"w = \\pm ({base.formatted()}) \\implies w_0 = {base.formatted()}, \\quad w_1 = {-base.real:+g} {-base.imag:+g}i".replace("+-", "-")
            }
        ]
        options = [base.formatted(), format_complex(base.real, -base.imag), format_complex(base.imag, base.real), format_complex(base.real + 1, base.imag)]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, base.formatted())

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "powers_roots",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": base.formatted(),
            "correct_real": base.real,
            "correct_imag": base.imag,
            "is_complex": True,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }

    else:  # de_moivre
        n = random.randint(3, 6)
        base = ComplexNum(1, 1)
        cur = ComplexNum(1, 0)
        for _ in range(n):
            cur = multiply(cur, base)
        res = cur

        question_text = f"Using De Moivre's theorem, evaluate $({base.formatted()})^{{{n}}}$."
        hint = "Convert 1+i to polar form: r = √2, θ = π/4 (45°), then apply (r·e^(iθ))^n = r^n·e^(inθ)."
        r_val = math.sqrt(2)
        r_pow_n = r_val ** n
        n_theta_str = f"{n}\\pi/4"

        steps = [
            {
                "step": "1",
                "title": "State De Moivre's Theorem",
                "description": "For any complex number in polar form $z = r(\\cos\\theta + i\\sin\\theta) = r e^{i\\theta}$ and integer $n$:",
                "latex": "z^n = [r(\\cos\\theta + i\\sin\\theta)]^n = r^n(\\cos n\\theta + i\\sin n\\theta) = r^n e^{i n\\theta}"
            },
            {
                "step": "2",
                "title": "Convert the base to polar coordinates",
                "description": "Calculate modulus $r$ and principal argument $\\theta$ of $1 + i$:",
                "latex": "r = \\sqrt{1^2 + 1^2} = \\sqrt{2}, \\quad \\theta = \\arctan(1/1) = \\frac{\\pi}{4}"
            },
            {
                "step": "3",
                "title": "Apply the theorem with power n",
                "description": f"Raise the modulus to power {n} and multiply the angle by {n}:",
                "latex": f"({base.formatted()})^{{{n}}} = (\\sqrt{{2}})^{{{n}}} \\left[\\cos\\left({n_theta_str}\\right) + i\\sin\\left({n_theta_str}\\right)\\right]"
            },
            {
                "step": "4",
                "title": "Evaluate trigonometric values and simplify",
                "description": "Convert back to standard rectangular form:",
                "latex": f"= {clean_number(r_pow_n)} \\left[\\cos\\left({n_theta_str}\\right) + i\\sin\\left({n_theta_str}\\right)\\right] = {res.formatted()}"
            }
        ]

        options = [
            res.formatted(),
            format_complex(-res.real, res.imag),
            format_complex(res.real, -res.imag),
            format_complex(res.imag, res.real)
        ]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, res.formatted())

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "powers_roots",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": res.formatted(),
            "correct_real": res.real,
            "correct_imag": res.imag,
            "is_complex": True,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }


def generate_polar_question(difficulty: str) -> Dict[str, Any]:
    """Generate polar representation and argument questions with complete steps."""
    cases = [
        (ComplexNum(1, 1), "45", "\\pi/4", math.sqrt(2)),
        (ComplexNum(0, 3), "90", "\\pi/2", 3.0),
        (ComplexNum(-2, 0), "180", "\\pi", 2.0),
        (ComplexNum(0, -4), "-90", "-\\pi/2", 4.0),
        (ComplexNum(1, -1), "-45", "-\\pi/4", math.sqrt(2)),
        (ComplexNum(-1, 1), "135", "3\\pi/4", math.sqrt(2)),
    ]
    z, deg_str, rad_str, mod_val = random.choice(cases)
    steps = []

    ask_arg = random.choice([True, False])
    if ask_arg:
        question_text = f"Find the principal argument $\\text{{Arg}}(z)$ in degrees for $z = {z.formatted()}$."
        hint = "Locate the number on the complex plane and determine the angle from the positive real axis."

        quadrant_info = ""
        if z.real > 0 and z.imag > 0:
            quadrant_info = "Quadrant I (a > 0, b > 0) \\implies \\theta = \\arctan(b/a)"
        elif z.real < 0 and z.imag > 0:
            quadrant_info = "Quadrant II (a < 0, b > 0) \\implies \\theta = \\arctan(b/a) + 180^\\circ"
        elif z.real < 0 and z.imag < 0:
            quadrant_info = "Quadrant III (a < 0, b < 0) \\implies \\theta = \\arctan(b/a) - 180^\\circ"
        elif z.real > 0 and z.imag < 0:
            quadrant_info = "Quadrant IV (a > 0, b < 0) \\implies \\theta = \\arctan(b/a)"
        elif z.real == 0 and z.imag > 0:
            quadrant_info = "Positive Imaginary Axis \\implies \\theta = 90^\\circ"
        elif z.real == 0 and z.imag < 0:
            quadrant_info = "Negative Imaginary Axis \\implies \\theta = -90^\\circ"
        elif z.real < 0 and z.imag == 0:
            quadrant_info = "Negative Real Axis \\implies \\theta = 180^\\circ"

        steps = [
            {
                "step": "1",
                "title": "Locate position on the Argand plane",
                "description": f"Examine the real part $a = {clean_number(z.real)}$ and imaginary part $b = {clean_number(z.imag)}$:",
                "latex": f"a = {clean_number(z.real)}, \\quad b = {clean_number(z.imag)} \\implies \\text{{{quadrant_info}}}"
            },
            {
                "step": "2",
                "title": "Recall the principal argument definition",
                "description": "The principal argument $\\text{Arg}(z)$ is the directed angle measured counter-clockwise from the positive real axis, constrained to $(-180^\\circ, 180^\\circ]$ (or $(-\\pi, \\pi]$ rad):",
                "latex": "\\text{Arg}(z) = \\text{atan2}(b, a)"
            },
            {
                "step": "3",
                "title": "Evaluate the angle",
                "description": f"Compute the angle for coordinates $({clean_number(z.real)}, {clean_number(z.imag)})$:",
                "latex": f"\\theta = {rad_str}\\text{{ rad}} = {deg_str}^\\circ"
            },
            {
                "step": "4",
                "title": "State the final principal argument",
                "description": "Express in degrees as requested:",
                "latex": f"\\text{{Arg}}({z.formatted()}) = {deg_str}^\\circ"
            }
        ]

        correct_answer = f"{deg_str}°"
        options = [f"{deg_str}°", f"{-int(deg_str)}°", f"{int(deg_str) + 90}°", f"{int(deg_str) - 90}°"]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, correct_answer)

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "polar_exponential",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "correct_real": float(deg_str),
            "correct_imag": 0.0,
            "is_complex": False,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }
    else:
        ans = clean_number(mod_val, 4)
        question_text = f"Determine the modulus $r = |z|$ for $z = {z.formatted()}$."
        hint = "Compute r = √(a² + b²)."
        a_sq = z.real ** 2
        b_sq = z.imag ** 2
        sum_sq = a_sq + b_sq

        steps = [
            {
                "step": "1",
                "title": "State the modulus formula",
                "description": "The modulus $r = |z|$ represents the Euclidean distance from the origin $(0, 0)$ to $(a, b)$ on the complex plane:",
                "latex": "r = |z| = \\sqrt{a^2 + b^2} \\quad \\text{where } z = a + bi"
            },
            {
                "step": "2",
                "title": "Identify the real and imaginary parts",
                "description": f"Extract components from $z = {z.formatted()}$:",
                "latex": f"a = \\text{{Re}}(z) = {clean_number(z.real)}, \\quad b = \\text{{Im}}(z) = {clean_number(z.imag)}"
            },
            {
                "step": "3",
                "title": "Substitute the values into the formula",
                "description": "Square both components under the radical sign:",
                "latex": f"r = \\sqrt{{({clean_number(z.real)})^2 + ({clean_number(z.imag)})^2}} = \\sqrt{{{clean_number(a_sq)} + {clean_number(b_sq)}}}"
            },
            {
                "step": "4",
                "title": "Simplify under the radical",
                "description": "Sum the squared terms:",
                "latex": f"= \\sqrt{{{clean_number(sum_sq)}}}"
            },
            {
                "step": "5",
                "title": "Evaluate the square root",
                "description": "Compute the principal non-negative root:",
                "latex": f"r = {ans}"
            }
        ]

        options = [ans, clean_number(mod_val + 1, 4), clean_number(mod_val * 2, 4), clean_number(mod_val / 2, 4)]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, ans)

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "polar_exponential",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": ans,
            "correct_real": mod_val,
            "correct_imag": 0.0,
            "is_complex": False,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }


def generate_equation_question(difficulty: str) -> Dict[str, Any]:
    """Generate linear or quadratic complex equation question with complete steps."""
    is_quadratic = (difficulty == "advanced") or (random.random() < 0.5 and difficulty == "intermediate")

    if not is_quadratic:
        # Linear: az + b = c -> z = (c - b) / a
        a = ComplexNum(random.randint(1, 3), random.randint(1, 2))
        z_sol = ComplexNum(random.randint(-3, 3), random.randint(-3, 3))
        b = ComplexNum(random.randint(-4, 4), random.randint(-4, 4))
        # c = a*z_sol + b
        c = add(multiply(a, z_sol), b)

        rhs = subtract(c, b)
        question_text = f"Solve for complex $z$: $({a.formatted()})z + ({b.formatted()}) = {c.formatted()}$."
        hint = "Subtract b from both sides, then divide by coefficient a."

        steps = [
            {
                "step": "1",
                "title": "Write the linear equation",
                "description": "Identify the linear complex relation in terms of $z$:",
                "latex": f"({a.formatted()})z + ({b.formatted()}) = {c.formatted()}"
            },
            {
                "step": "2",
                "title": "Isolate the z term",
                "description": "Subtract the constant term from both sides:",
                "latex": f"({a.formatted()})z = ({c.formatted()}) - ({b.formatted()}) = {rhs.formatted()}"
            },
            {
                "step": "3",
                "title": "Divide by the coefficient of z",
                "description": "Divide both sides by $a$:",
                "latex": f"z = \\frac{{{rhs.formatted()}}}{{{a.formatted()}}}"
            },
            {
                "step": "4",
                "title": "Realize the denominator using conjugates",
                "description": f"Multiply numerator and denominator by $\\overline{{{a.formatted()}}} = {conjugate(a).formatted()}$:",
                "latex": f"z = \\frac{{({rhs.formatted()})({conjugate(a).formatted()})}}{{{clean_number(a.real**2 + a.imag**2)}}} = {z_sol.formatted()}"
            }
        ]

        options = [
            z_sol.formatted(),
            format_complex(-z_sol.real, z_sol.imag),
            format_complex(z_sol.real, -z_sol.imag),
            format_complex(z_sol.imag, z_sol.real)
        ]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, z_sol.formatted())

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "equations",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": z_sol.formatted(),
            "correct_real": z_sol.real,
            "correct_imag": z_sol.imag,
            "is_complex": True,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }
    else:
        k_val = random.randint(1, 3)
        m_val = random.randint(1, 3)
        b_coeff = -2 * k_val
        c_coeff = k_val**2 + m_val**2
        delta = b_coeff**2 - 4 * c_coeff
        sqrt_delta_val = 2 * m_val

        question_text = f"Find a root of the quadratic equation: $z^2 {b_coeff:+g}z + {c_coeff} = 0$."
        hint = "Use the quadratic formula: z = (-b ± √Δ) / 2a with discriminant Δ = b² - 4ac."

        sol_root = ComplexNum(float(k_val), float(m_val))

        steps = [
            {
                "step": "1",
                "title": "Identify quadratic coefficients",
                "description": "Compare with standard quadratic form $az^2 + bz + c = 0$:",
                "latex": f"a = 1, \\quad b = {b_coeff}, \\quad c = {c_coeff}"
            },
            {
                "step": "2",
                "title": "Compute the discriminant Δ = b² - 4ac",
                "description": "Evaluate $\\Delta$:",
                "latex": f"\\Delta = ({b_coeff})^2 - 4(1)({c_coeff}) = {b_coeff**2} - {4*c_coeff} = {delta}"
            },
            {
                "step": "3",
                "title": "Compute the square roots of the discriminant",
                "description": f"Since $\\Delta = {delta} < 0$, its square root is imaginary:",
                "latex": f"\\sqrt{{\\Delta}} = \\sqrt{{{delta}}} = \\pm {sqrt_delta_val}i"
            },
            {
                "step": "4",
                "title": "Apply the quadratic formula",
                "description": "Substitute $a, b, \\sqrt{\\Delta}$ into $z = (-b \\pm \\sqrt{\\Delta}) / 2a$:",
                "latex": f"z = \\frac{{-({b_coeff}) \\pm {sqrt_delta_val}i}}{{2(1)}} = \\frac{{{ -b_coeff } \\pm {sqrt_delta_val}i}}{{2}} = {k_val} \\pm {m_val}i"
            },
            {
                "step": "5",
                "title": "Conclude the roots",
                "description": "The two roots are conjugate pairs:",
                "latex": f"z_1 = {sol_root.formatted()}, \\quad z_2 = {k_val} - {m_val}i"
            }
        ]

        options = [
            sol_root.formatted(),
            format_complex(-sol_root.real, sol_root.imag),
            format_complex(sol_root.real + 1, sol_root.imag),
            format_complex(sol_root.real, sol_root.imag + 1)
        ]
        random.shuffle(options)
        solution_text = _build_solution_text(steps, sol_root.formatted())

        return {
            "id": str(uuid.uuid4())[:8],
            "topic": "equations",
            "difficulty": difficulty,
            "type": "multiple_choice",
            "question": question_text,
            "options": options,
            "correct_answer": sol_root.formatted(),
            "correct_real": sol_root.real,
            "correct_imag": sol_root.imag,
            "is_complex": True,
            "hint": hint,
            "solution": solution_text,
            "steps": steps
        }


def generate_question(topic: str = "all", difficulty: str = "beginner") -> Dict[str, Any]:
    """Generate a question given topic and difficulty."""
    if topic not in TOPICS and topic != "all":
        topic = "all"
    if difficulty not in DIFFICULTIES:
        difficulty = "beginner"

    chosen_topic = topic if topic != "all" else random.choice(TOPICS)

    if chosen_topic == "arithmetic":
        return generate_arithmetic_question(difficulty)
    elif chosen_topic == "conjugate_modulus":
        return generate_conjugate_modulus_question(difficulty)
    elif chosen_topic == "powers_roots":
        return generate_powers_roots_question(difficulty)
    elif chosen_topic == "polar_exponential":
        return generate_polar_question(difficulty)
    elif chosen_topic == "equations":
        return generate_equation_question(difficulty)
    else:
        return generate_arithmetic_question(difficulty)


def check_user_answer(question_data: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    """Verify user answer using numerical tolerance for components or exact option match."""
    if not user_input or not user_input.strip():
        return {
            "correct": False,
            "feedback": "Please enter or select an answer before checking.",
            "user_parsed": None,
            "correct_answer": question_data["correct_answer"],
            "solution": question_data.get("solution", ""),
            "steps": question_data.get("steps", [])
        }

    user_str = user_input.strip()
    correct_ans = question_data["correct_answer"].strip()
    is_complex = question_data.get("is_complex", True)
    steps = question_data.get("steps", [])

    # 1. Exact string match (e.g. multiple choice selection)
    clean_user = user_str.replace(" ", "").rstrip("°")
    clean_corr = correct_ans.replace(" ", "").rstrip("°")
    if clean_user.lower() == clean_corr.lower():
        return {
            "correct": True,
            "feedback": "Correct! Excellent mathematical reasoning.",
            "user_parsed": correct_ans,
            "correct_answer": correct_ans,
            "solution": question_data.get("solution", ""),
            "steps": steps
        }

    # 2. Mathematical evaluation with tolerance
    if is_complex:
        try:
            parsed_c = parse_complex_expression(user_str)
            target_r = question_data.get("correct_real", 0.0)
            target_i = question_data.get("correct_imag", 0.0)

            diff_r = abs(parsed_c.real - target_r)
            diff_i = abs(parsed_c.imag - target_i)

            if diff_r < 0.05 and diff_i < 0.05:
                return {
                    "correct": True,
                    "feedback": f"Correct! Your answer {format_complex(parsed_c.real, parsed_c.imag)} matches the required value.",
                    "user_parsed": format_complex(parsed_c.real, parsed_c.imag),
                    "correct_answer": correct_ans,
                    "solution": question_data.get("solution", ""),
                    "steps": steps
                }
            else:
                return {
                    "correct": False,
                    "feedback": f"Not quite. You entered {format_complex(parsed_c.real, parsed_c.imag)}, but the expected result is {correct_ans}.",
                    "user_parsed": format_complex(parsed_c.real, parsed_c.imag),
                    "correct_answer": correct_ans,
                    "solution": question_data.get("solution", ""),
                    "steps": steps
                }
        except ParseError:
            pass

    # 3. Numeric float match
    try:
        val = float(clean_user)
        target_r = question_data.get("correct_real", 0.0)
        if abs(val - target_r) < 0.05:
            return {
                "correct": True,
                "feedback": "Correct! Well done.",
                "user_parsed": str(val),
                "correct_answer": correct_ans,
                "solution": question_data.get("solution", ""),
                "steps": steps
            }
    except ValueError:
        pass

    return {
        "correct": False,
        "feedback": f"Incorrect. Your answer was '{user_input}', but the correct answer is {correct_ans}.",
        "user_parsed": user_input,
        "correct_answer": correct_ans,
        "solution": question_data.get("solution", ""),
        "steps": steps
    }
