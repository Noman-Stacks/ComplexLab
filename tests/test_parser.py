"""Tests for Safe Mathematical Expression Parser
"""
import pytest
import math
from src.parser import parse_complex_expression, parse_rectangular_inputs, parse_number_list, ParseError


def test_standard_formats():
    assert parse_complex_expression("3 + 4i") == complex(3, 4)
    assert parse_complex_expression("3 - 4i") == complex(3, -4)
    assert parse_complex_expression("-2 + 5i") == complex(-2, 5)
    assert parse_complex_expression("7i") == complex(0, 7)
    assert parse_complex_expression("-7i") == complex(0, -7)
    assert parse_complex_expression("5") == complex(5, 0)
    assert parse_complex_expression("-3") == complex(-3, 0)
    assert parse_complex_expression("i") == complex(0, 1)
    assert parse_complex_expression("-i") == complex(0, -1)
    assert parse_complex_expression("0") == complex(0, 0)
    assert parse_complex_expression("0 + 0i") == complex(0, 0)


def test_j_notation():
    assert parse_complex_expression("3 + 4j") == complex(3, 4)
    assert parse_complex_expression("7j") == complex(0, 7)
    assert parse_complex_expression("-j") == complex(0, -1)
    assert parse_complex_expression("j") == complex(0, 1)


def test_decimals_and_fractions():
    c1 = parse_complex_expression("1.5 + 2.75i")
    assert abs(c1.real - 1.5) < 1e-9 and abs(c1.imag - 2.75) < 1e-9

    c2 = parse_complex_expression("1/2 + 3/4i")
    assert abs(c2.real - 0.5) < 1e-9 and abs(c2.imag - 0.75) < 1e-9


def test_parentheses_and_arithmetic_in_expressions():
    c = parse_complex_expression("(2 - 3i) * (1 + i)")
    # (2-3i)(1+i) = 2 + 2i - 3i + 3 = 5 - i
    assert abs(c.real - 5.0) < 1e-9 and abs(c.imag - (-1.0)) < 1e-9


def test_rectangular_inputs_mode_a():
    assert parse_rectangular_inputs("3", "4") == complex(3, 4)
    assert parse_rectangular_inputs("-2.5", "6.25") == complex(-2.5, 6.25)
    assert parse_rectangular_inputs("1/2", "-3/4") == complex(0.5, -0.75)
    assert parse_rectangular_inputs(None, "5") == complex(0, 5)
    assert parse_rectangular_inputs("7", "") == complex(7, 0)


def test_parse_number_list():
    lst = parse_number_list("1+2i, 3-4i; 5")
    assert len(lst) == 3
    assert lst[0] == complex(1, 2)
    assert lst[1] == complex(3, -4)
    assert lst[2] == complex(5, 0)


def test_malformed_and_security_rejections():
    with pytest.raises(ParseError):
        parse_complex_expression("")

    with pytest.raises(ParseError):
        parse_complex_expression("import os; os.system('calc')")

    with pytest.raises(ParseError):
        parse_complex_expression("__import__('sys')")

    with pytest.raises(ParseError):
        parse_complex_expression("eval('3+4')")

    with pytest.raises(ParseError):
        parse_complex_expression("3 ++* 4i")

    with pytest.raises(ParseError):
        parse_complex_expression("1 / 0")
