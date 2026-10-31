"""Tests for Flask REST API Endpoints and Validation
"""
import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_page_routes(client):
    # Test index page
    res_index = client.get("/")
    assert res_index.status_code == 200
    assert b"ComplexLab" in res_index.data
    assert b"Explore Complex Numbers. Solve with Confidence." in res_index.data

    # Test learn page
    res_learn = client.get("/learn")
    assert res_learn.status_code == 200
    assert b"Mathematics Learning Center" in res_learn.data

    # Test practice page
    res_practice = client.get("/practice")
    assert res_practice.status_code == 200
    assert b"Practice &amp; Exercises" in res_practice.data or b"Practice & Exercises" in res_practice.data

    # Test about page
    res_about = client.get("/about")
    assert res_about.status_code == 200
    assert b"About ComplexLab" in res_about.data
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["app"] == "ComplexLab"


def test_calculate_multiply(client):
    payload = {
        "operation": "multiply",
        "z1": "3 + 4i",
        "z2": "2 - i"
    }
    res = client.post("/api/calculate", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["result"]["formatted"] == "10 + 5i"
    assert len(data["steps"]) > 0


def test_calculate_divide_zero_error(client):
    payload = {
        "operation": "divide",
        "z1": "3 + 4i",
        "z2": "0"
    }
    res = client.post("/api/calculate", json=payload)
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False
    assert "zero" in data["error"].lower()


def test_calculate_unary_conjugate(client):
    payload = {
        "operation": "conjugate",
        "z1": "3 + 4i"
    }
    res = client.post("/api/calculate", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["result"]["formatted"] == "3 - 4i"


def test_calculate_powers_of_i(client):
    payload = {
        "operation": "powers_of_i",
        "exponent": 105
    }
    res = client.post("/api/calculate", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["result_str"] == "i"


def test_convert_endpoint(client):
    payload = {
        "mode": "rectangular_to_all",
        "z": "1 + i"
    }
    res = client.post("/api/convert", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert abs(data["result"]["argument_degrees"] - 45.0) < 1e-4


def test_roots_endpoint(client):
    payload = {
        "type": "roots_of_unity",
        "n": 4
    }
    res = client.post("/api/roots", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["result"]["roots"]) == 4


def test_equations_endpoint(client):
    payload = {
        "type": "quadratic",
        "a": "1",
        "b": "-2",
        "c": "5"
    }
    res = client.post("/api/equation/solve", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["result"]["roots"]) == 2


def test_bad_request_payloads(client):
    # Missing operation
    res1 = client.post("/api/calculate", json={})
    assert res1.status_code == 400

    # Unsupported operation
    res2 = client.post("/api/calculate", json={"operation": "unsupported_xyz", "z1": "1"})
    assert res2.status_code == 400

    # Malformed syntax
    res3 = client.post("/api/calculate", json={"operation": "add", "z1": "3 ++* 4i", "z2": "1"})
    assert res3.status_code == 400
