"""Tests for Linear and Quadratic Complex Equation Solving
"""
from src.complex_engine import ComplexNum, multiply, add
from src.equations import solve_linear, solve_quadratic


def test_solve_linear_equation():
    # Solve (2 + i)z + 3 = 4 - i
    # (2 + i)z = 1 - i
    # z = (1 - i) / (2 + i) = (1 - i)(2 - i)/5 = (2 - 3i - 1)/5 = 0.2 - 0.6i
    a = ComplexNum(2.0, 1.0)
    b = ComplexNum(3.0, 0.0)
    c = ComplexNum(4.0, -1.0)

    res = solve_linear(a, b, c)
    assert res["solvable"] is True
    sol = res["solution"]
    assert abs(sol["real"] - 0.2) < 1e-6
    assert abs(sol["imaginary"] - (-0.6)) < 1e-6

    # Verify solution satisfies equation: a*z + b == c
    z_sol = ComplexNum(sol["real"], sol["imaginary"])
    lhs = add(multiply(a, z_sol), b)
    assert abs(lhs.real - c.real) < 1e-6
    assert abs(lhs.imag - c.imag) < 1e-6


def test_solve_linear_degenerate():
    # 0*z + 3 = 5 -> no solution
    res1 = solve_linear(ComplexNum(0, 0), ComplexNum(3, 0), ComplexNum(5, 0))
    assert res1["solvable"] is False

    # 0*z + 3 = 3 -> infinite solutions
    res2 = solve_linear(ComplexNum(0, 0), ComplexNum(3, 0), ComplexNum(3, 0))
    assert res2["infinite_solutions"] is True


def test_solve_quadratic_complex_roots():
    # Solve z^2 - 2z + 5 = 0 -> roots are 1 + 2i and 1 - 2i
    a = ComplexNum(1.0, 0.0)
    b = ComplexNum(-2.0, 0.0)
    c = ComplexNum(5.0, 0.0)

    res = solve_quadratic(a, b, c)
    assert res["solvable"] is True
    assert len(res["roots"]) == 2

    r1, r2 = res["roots"][0], res["roots"][1]
    reals = sorted([r1["real"], r2["real"]])
    imags = sorted([abs(r1["imaginary"]), abs(r2["imaginary"])])
    assert abs(reals[0] - 1.0) < 1e-6
    assert abs(reals[1] - 1.0) < 1e-6
    assert abs(imags[0] - 2.0) < 1e-6
    assert abs(imags[1] - 2.0) < 1e-6


def test_solve_quadratic_repeated_root():
    # (z - (1+i))^2 = z^2 - 2(1+i)z + 2i = 0
    # a = 1, b = -2-2i, c = 2i -> root is 1+i
    a = ComplexNum(1.0, 0.0)
    b = ComplexNum(-2.0, -2.0)
    c = ComplexNum(0.0, 2.0)

    res = solve_quadratic(a, b, c)
    assert res["is_repeated"] is True
    assert abs(res["roots"][0]["real"] - 1.0) < 1e-6
    assert abs(res["roots"][0]["imaginary"] - 1.0) < 1e-6
