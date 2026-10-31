"""ComplexLab Flask Application
Web server and REST API for Complex Number Calculator & Mathematics Learning Platform.
"""
import os
import sys
import traceback
from flask import Flask, render_template, request, jsonify

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.complex_engine import (
    ComplexNum, add, subtract, multiply, divide, negate, equals,
    sum_multiple, product_multiple, conjugate, double_conjugate,
    real_part, imag_part, modulus, argument, reciprocal,
    verify_conjugate_identities, integer_power, powers_of_i,
    distance, normalize, verify_multiplicative_inverse, product_with_conjugate,
    complex_power
)
from src.parser import parse_complex_expression, parse_rectangular_inputs, parse_number_list, ParseError
from src.conversions import rectangular_to_all, polar_to_all, convert_angles
from src.roots import get_square_roots_detailed, get_nth_roots_detailed, get_roots_of_unity_detailed, apply_de_moivre
from src.equations import solve_linear, solve_quadratic
from src.explanations import (
    explain_addition, explain_subtraction, explain_multiplication, explain_division,
    explain_modulus, explain_argument, explain_reciprocal, explain_powers_of_i,
    explain_nth_roots, explain_de_moivre
)
from src.practice import generate_question, check_user_answer
from src.formatter import clean_number, format_complex

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24).hex()


def _extract_complex(data: dict, prefix: str = "z1") -> ComplexNum:
    """Extract complex number from request body supporting both Mode A (rectangular) and Mode B (expression)."""
    # Mode B: expression string
    expr_key = prefix
    if expr_key in data and data[expr_key] is not None and str(data[expr_key]).strip() != "":
        return ComplexNum.from_complex(parse_complex_expression(str(data[expr_key])))

    # Mode A: separate real and imag fields
    real_key = f"{prefix}_real"
    imag_key = f"{prefix}_imag"
    if real_key in data or imag_key in data:
        r_val = data.get(real_key, 0.0)
        i_val = data.get(imag_key, 0.0)
        return ComplexNum.from_complex(parse_rectangular_inputs(r_val, i_val))

    raise ParseError(f"Missing input for complex number '{prefix}'.")


# ==============================================================================
# PAGE ROUTES
# ==============================================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/practice")
def practice():
    return render_template("practice.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "app": "ComplexLab",
        "version": "1.0.0",
        "message": "Explore Complex Numbers. Solve with Confidence."
    })


@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "error": "Invalid or missing JSON payload."}), 400

        operation = data.get("operation")
        if not operation:
            return jsonify({"success": False, "error": "Operation is required."}), 400

        operation = str(operation).lower().strip()
        precision = int(data.get("precision", 6))
        precision = max(2, min(precision, 12))

        # Handle powers of i separately
        if operation == "powers_of_i":
            k = int(data.get("exponent", data.get("k", 1)))
            pow_data = powers_of_i(k)
            steps = explain_powers_of_i(k, pow_data)
            return jsonify({
                "success": True,
                "operation": operation,
                "inputs": {"exponent": k},
                "result": pow_data["result_complex"],
                "result_str": pow_data["result_str"],
                "steps": steps
            })

        # Multi-number sum and product
        if operation in ["sum_multiple", "product_multiple"]:
            numbers_raw = data.get("numbers", "")
            z_list = [ComplexNum.from_complex(c) for c in parse_number_list(numbers_raw)]
            if operation == "sum_multiple":
                res = sum_multiple(z_list)
                title = "Sum of multiple complex numbers"
            else:
                res = product_multiple(z_list)
                title = "Product of multiple complex numbers"

            steps = [
                {"step": "1", "title": "List of Inputs", "latex": ", \\quad ".join([z.formatted() for z in z_list])},
                {"step": "2", "title": "Calculated Result", "latex": f"\\text{{Result}} = {res.formatted()}"}
            ]
            return jsonify({
                "success": True,
                "operation": operation,
                "inputs": {"numbers": [z.to_dict() for z in z_list]},
                "result": res.to_dict(precision),
                "steps": steps
            })

        # Unary operations (only z1 needed)
        unary_ops = [
            "conjugate", "double_conjugate", "negate", "reciprocal",
            "modulus", "argument", "normalize", "verify_identities",
            "verify_inverse", "product_with_conjugate", "real_part", "imag_part"
        ]

        if operation in unary_ops:
            z1 = _extract_complex(data, "z1")

            if operation == "conjugate":
                res = conjugate(z1)
                steps = [
                    {"step": "1", "title": "Given complex number", "latex": f"z = {z1.formatted()}"},
                    {"step": "2", "title": "Apply complex conjugate definition", "latex": "\\overline{a + bi} = a - bi"},
                    {"step": "3", "title": "Invert imaginary sign", "latex": f"\\overline{{{z1.formatted()}}} = {res.formatted()}"}
                ]
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res.to_dict(precision),
                    "steps": steps
                })

            elif operation == "double_conjugate":
                res, is_id = double_conjugate(z1)
                steps = [
                    {"step": "1", "title": "First Conjugate", "latex": f"\\overline{{z}} = {conjugate(z1).formatted()}"},
                    {"step": "2", "title": "Second Conjugate", "latex": f"\\overline{{\\overline{{z}}}} = \\overline{{{conjugate(z1).formatted()}}} = {res.formatted()}"},
                    {"step": "3", "title": "Verify Identity", "latex": f"\\overline{{\\overline{{z}}}} = z \\implies {res.formatted()} = {z1.formatted()} \\quad (\\text{{Holds: }} {is_id})"}
                ]
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res.to_dict(precision),
                    "identity_verified": is_id,
                    "steps": steps
                })

            elif operation == "negate":
                res = negate(z1)
                steps = [
                    {"step": "1", "title": "Given complex number", "latex": f"z = {z1.formatted()}"},
                    {"step": "2", "title": "Multiply by -1", "latex": f"-z = -({z1.formatted()}) = {res.formatted()}"}
                ]
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res.to_dict(precision),
                    "steps": steps
                })

            elif operation == "reciprocal":
                res = reciprocal(z1)
                steps = explain_reciprocal(z1, res)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res.to_dict(precision),
                    "steps": steps
                })

            elif operation == "modulus":
                mod_val = modulus(z1)
                steps = explain_modulus(z1, mod_val)
                res_obj = z1.to_dict(precision)
                res_obj["value"] = round(mod_val, precision)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res_obj,
                    "steps": steps
                })

            elif operation == "argument":
                rad, deg = argument(z1)
                steps = explain_argument(z1, rad or 0.0, deg or 0.0)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": {
                        "radians": round(rad, precision) if rad is not None else None,
                        "degrees": round(deg, 2) if deg is not None else None,
                        "is_zero": z1.is_zero
                    },
                    "steps": steps
                })

            elif operation == "normalize":
                res = normalize(z1)
                steps = [
                    {"step": "1", "title": "Modulus calculation", "latex": f"|z| = {clean_number(z1.modulus, 4)}"},
                    {"step": "2", "title": "Divide z by |z|", "latex": f"\\hat{{z}} = \\frac{{{z1.formatted()}}}{{{clean_number(z1.modulus, 4)}}} = {res.formatted()}"},
                    {"step": "3", "title": "Verify unit modulus", "latex": f"|\\hat{{z}}| = {clean_number(res.modulus, 6)} = 1"}
                ]
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": res.to_dict(precision),
                    "steps": steps
                })

            elif operation == "verify_identities":
                identities = verify_conjugate_identities(z1)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": identities,
                    "steps": [
                        {"step": "Identity 1", "title": "Sum with conjugate", "latex": f"z + \\bar{{z}} = {identities['identity_1']['lhs']} = {identities['identity_1']['rhs']}"},
                        {"step": "Identity 2", "title": "Difference with conjugate", "latex": f"z - \\bar{{z}} = {identities['identity_2']['lhs']} = {identities['identity_2']['rhs']}"},
                        {"step": "Identity 3", "title": "Product with conjugate", "latex": f"z \\cdot \\bar{{z}} = {identities['identity_3']['lhs']} = |z|^2 = {identities['identity_3']['rhs']}"}
                    ]
                })

            elif operation == "verify_inverse":
                data_inv = verify_multiplicative_inverse(z1)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": data_inv,
                    "steps": [
                        {"step": "1", "title": "Calculate reciprocal", "latex": f"z^{{-1}} = {data_inv['inverse']['formatted']}"},
                        {"step": "2", "title": "Multiply z by z^(-1)", "latex": f"({z1.formatted()})({data_inv['inverse']['formatted']}) = {data_inv['product']['formatted']}"},
                        {"step": "3", "title": "Conclusion", "latex": "\\text{Identity holds: } z \\cdot z^{-1} = 1"}
                    ]
                })

            elif operation == "product_with_conjugate":
                p_data = product_with_conjugate(z1)
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": p_data["product"],
                    "modulus_squared": p_data["modulus_squared"],
                    "steps": [
                        {"step": "1", "title": "Find conjugate", "latex": f"\\bar{{z}} = {p_data['conjugate']['formatted']}"},
                        {"step": "2", "title": "Multiply z by conjugate", "latex": f"({z1.formatted()})({p_data['conjugate']['formatted']}) = {p_data['product']['formatted']}"},
                        {"step": "3", "title": "Check |z|²", "latex": f"|z|^2 = ({clean_number(z1.real)})^2 + ({clean_number(z1.imag)})^2 = {clean_number(p_data['modulus_squared'])}"}
                    ]
                })

            elif operation in ["real_part", "imag_part"]:
                val = real_part(z1) if operation == "real_part" else imag_part(z1)
                title = "Real Part Re(z)" if operation == "real_part" else "Imaginary Part Im(z)"
                latex_sym = "\\text{Re}(z)" if operation == "real_part" else "\\text{Im}(z)"
                return jsonify({
                    "success": True,
                    "operation": operation,
                    "inputs": {"z1": z1.to_dict()},
                    "result": {"value": val, "formatted": clean_number(val)},
                    "steps": [
                        {"step": "1", "title": "Given complex number", "latex": f"z = {z1.formatted()}"},
                        {"step": "2", "title": f"Extract {title}", "latex": f"{latex_sym} = {clean_number(val)}"}
                    ]
                })

        # Binary operations (requiring z1 and z2 or exponent n)
        z1 = _extract_complex(data, "z1")

        if operation in ["power", "pow"]:
            # Check if exponent is integer n or complex z2
            if "exponent" in data or "n" in data:
                n = int(data.get("exponent", data.get("n", 2)))
                res = integer_power(z1, n)
                steps = [
                    {"step": "1", "title": "Given base and exponent", "latex": f"z = {z1.formatted()}, \\quad n = {n}"},
                    {"step": "2", "title": "Apply polar exponentiation or binomial expansion", "latex": f"({z1.formatted()})^{{{n}}} = {res.formatted()}"}
                ]
                return jsonify({
                    "success": True,
                    "operation": "power",
                    "inputs": {"z1": z1.to_dict(), "exponent": n},
                    "result": res.to_dict(precision),
                    "steps": steps
                })
            else:
                z2 = _extract_complex(data, "z2")
                res = complex_power(z1, z2)
                steps = [
                    {"step": "1", "title": "Formula for complex exponentiation", "latex": "z_1^{z_2} = \\exp(z_2 \\cdot \\text{Ln}(z_1))"},
                    {"step": "2", "title": "Principal value result", "latex": f"({z1.formatted()})^{{({z2.formatted()})}} = {res.formatted()}"}
                ]
                return jsonify({
                    "success": True,
                    "operation": "power",
                    "inputs": {"z1": z1.to_dict(), "z2": z2.to_dict()},
                    "result": res.to_dict(precision),
                    "steps": steps
                })

        # Standard binary operations: add, subtract, multiply, divide, equals, distance
        z2 = _extract_complex(data, "z2")

        if operation in ["add", "+"]:
            res = add(z1, z2)
            steps = explain_addition(z1, z2, res)
        elif operation in ["subtract", "-"]:
            res = subtract(z1, z2)
            steps = explain_subtraction(z1, z2, res)
        elif operation in ["multiply", "*", "times"]:
            res = multiply(z1, z2)
            steps = explain_multiplication(z1, z2, res)
        elif operation in ["divide", "/"]:
            res = divide(z1, z2)
            steps = explain_division(z1, z2, res)
        elif operation in ["equals", "=="]:
            eq = equals(z1, z2)
            steps = [
                {"step": "1", "title": "Compare Real Parts", "latex": f"\\text{{Re}}(z_1) = {clean_number(z1.real)} \\quad \\text{{vs}} \\quad \\text{{Re}}(z_2) = {clean_number(z2.real)}"},
                {"step": "2", "title": "Compare Imaginary Parts", "latex": f"\\text{{Im}}(z_1) = {clean_number(z1.imag)} \\quad \\text{{vs}} \\quad \\text{{Im}}(z_2) = {clean_number(z2.imag)}"},
                {"step": "3", "title": "Conclusion", "latex": f"z_1 = z_2 \\quad (\\text{{Result: }} {eq})"}
            ]
            return jsonify({
                "success": True,
                "operation": operation,
                "inputs": {"z1": z1.to_dict(), "z2": z2.to_dict()},
                "result": {"are_equal": eq, "formatted": str(eq)},
                "steps": steps
            })
        elif operation == "distance":
            dist_val = distance(z1, z2)
            diff = subtract(z1, z2)
            steps = [
                {"step": "1", "title": "Distance formula", "latex": "d(z_1, z_2) = |z_1 - z_2|"},
                {"step": "2", "title": "Difference vector", "latex": f"z_1 - z_2 = ({z1.formatted()}) - ({z2.formatted()}) = {diff.formatted()}"},
                {"step": "3", "title": "Modulus of difference", "latex": f"|{diff.formatted()}| = \\sqrt{{({clean_number(diff.real)})^2 + ({clean_number(diff.imag)})^2}} = {clean_number(dist_val, 6)}"}
            ]
            return jsonify({
                "success": True,
                "operation": operation,
                "inputs": {"z1": z1.to_dict(), "z2": z2.to_dict()},
                "result": {"distance": round(dist_val, precision), "formatted": clean_number(dist_val, precision)},
                "steps": steps
            })
        else:
            return jsonify({"success": False, "error": f"Unsupported mathematical operation: '{operation}'"}), 400

        return jsonify({
            "success": True,
            "operation": operation,
            "inputs": {"z1": z1.to_dict(), "z2": z2.to_dict()},
            "result": res.to_dict(precision),
            "steps": steps
        })

    except ZeroDivisionError as e:
        return jsonify({"success": False, "error": str(e)}), 422
    except ParseError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "An unexpected calculation error occurred. Please verify your inputs."}), 500


@app.route("/api/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json(silent=True) or {}
        mode = data.get("mode", "rectangular_to_all")

        if mode == "rectangular_to_all":
            z = _extract_complex(data, "z")
            res = rectangular_to_all(z)
            return jsonify({"success": True, "mode": mode, "result": res})

        elif mode == "polar_to_all":
            r = float(data.get("r", 1.0))
            theta = float(data.get("theta", 0.0))
            unit = data.get("unit", "radians")
            res = polar_to_all(r, theta, angle_unit=unit)
            return jsonify({"success": True, "mode": mode, "result": res})

        elif mode == "angle":
            val = float(data.get("value", 0.0))
            unit = data.get("unit", "degrees")
            res = convert_angles(val, from_unit=unit)
            return jsonify({"success": True, "mode": mode, "result": res})

        else:
            return jsonify({"success": False, "error": f"Invalid conversion mode: '{mode}'"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/roots", methods=["POST"])
def roots():
    try:
        data = request.get_json(silent=True) or {}
        root_type = data.get("type", "nth_roots")

        if root_type == "square_roots":
            z = _extract_complex(data, "z")
            details = get_square_roots_detailed(z)
            steps = [
                {"step": "1", "title": "Recall square root formula", "latex": "\\sqrt{z} = \\pm \\sqrt{r} e^{i\\theta/2}"},
                {"step": "2", "title": "Principal square root (w₀)", "latex": f"w_0 = {details['roots'][0]['formatted']}"},
            ]
            if len(details["roots"]) > 1:
                steps.append({"step": "3", "title": "Second square root (w₁ = -w₀)", "latex": f"w_1 = {details['roots'][1]['formatted']}"})
            return jsonify({"success": True, "type": root_type, "result": details, "steps": steps})

        elif root_type == "nth_roots":
            z = _extract_complex(data, "z")
            n = int(data.get("n", 3))
            details = get_nth_roots_detailed(z, n)
            steps = explain_nth_roots(z, n, details)
            return jsonify({"success": True, "type": root_type, "result": details, "steps": steps})

        elif root_type == "roots_of_unity":
            n = int(data.get("n", 4))
            details = get_roots_of_unity_detailed(n)
            one = ComplexNum(1.0, 0.0)
            steps = explain_nth_roots(one, n, details)
            return jsonify({"success": True, "type": root_type, "result": details, "steps": steps})

        elif root_type == "de_moivre":
            z = _extract_complex(data, "z")
            n = int(data.get("n", 2))
            details = apply_de_moivre(z, n)
            steps = explain_de_moivre(z, n, details)
            return jsonify({"success": True, "type": root_type, "result": details, "steps": steps})

        else:
            return jsonify({"success": False, "error": f"Invalid root operation type: '{root_type}'"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/equation/solve", methods=["POST"])
def solve_equation():
    try:
        data = request.get_json(silent=True) or {}
        eq_type = data.get("type", "linear")

        if eq_type == "linear":
            a = _extract_complex(data, "a")
            b = _extract_complex(data, "b")
            c = _extract_complex(data, "c")
            res = solve_linear(a, b, c)
            return jsonify({"success": True, "type": eq_type, "result": res, "steps": res.get("steps", [])})

        elif eq_type == "quadratic":
            a = _extract_complex(data, "a")
            b = _extract_complex(data, "b")
            c = _extract_complex(data, "c")
            res = solve_quadratic(a, b, c)
            return jsonify({"success": True, "type": eq_type, "result": res, "steps": res.get("steps", [])})

        else:
            return jsonify({"success": False, "error": f"Unsupported equation type: '{eq_type}'. Must be 'linear' or 'quadratic'."}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/practice/generate", methods=["POST"])
def practice_generate():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get("topic", "all")
        difficulty = data.get("difficulty", "beginner")
        q = generate_question(topic=topic, difficulty=difficulty)
        return jsonify({"success": True, "question": q})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/practice/check", methods=["POST"])
def practice_check():
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question")
        user_answer = data.get("answer", "")
        if not question:
            return jsonify({"success": False, "error": "Question specification is missing."}), 400

        result = check_user_answer(question, user_answer)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
