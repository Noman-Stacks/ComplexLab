"""Tests for Practice Generator and User Answer Verification
"""
from src.practice import generate_question, check_user_answer


def test_question_generation():
    topics = ["arithmetic", "conjugate_modulus", "polar_exponential", "powers_roots", "equations"]
    diffs = ["beginner", "intermediate", "advanced"]

    for t in topics:
        for d in diffs:
            q = generate_question(topic=t, difficulty=d)
            assert "question" in q
            assert "correct_answer" in q
            assert "hint" in q
            assert "solution" in q
            assert "steps" in q
            assert len(q["steps"]) >= 2
            for s in q["steps"]:
                assert "step" in s
                assert "title" in s
                assert "latex" in s


def test_answer_checker_exact_string():
    q = {
        "id": "test1",
        "type": "multiple_choice",
        "correct_answer": "3 + 4i",
        "correct_real": 3.0,
        "correct_imag": 4.0,
        "is_complex": True
    }
    res_correct = check_user_answer(q, "3 + 4i")
    assert res_correct["correct"] is True

    res_spaces = check_user_answer(q, "3+4i")
    assert res_spaces["correct"] is True

    res_wrong = check_user_answer(q, "3 - 4i")
    assert res_wrong["correct"] is False


def test_answer_checker_numeric_tolerance():
    q = {
        "id": "test2",
        "type": "free_input",
        "correct_answer": "1.414",
        "correct_real": 1.41421356,
        "correct_imag": 0.0,
        "is_complex": False
    }
    # User provides 1.41
    res = check_user_answer(q, "1.41")
    assert res["correct"] is True


def test_answer_checker_complex_tolerance():
    q = {
        "id": "test3",
        "type": "free_input",
        "correct_answer": "0.5 + 0.866i",
        "correct_real": 0.5,
        "correct_imag": 0.866025,
        "is_complex": True
    }
    res = check_user_answer(q, "0.5 + 0.87i")
    assert res["correct"] is True
