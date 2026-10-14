
from app import app, classify_level


def test_normal_level():
    assert classify_level(65)[0] == "NORMAL"


def test_low_water():
    assert classify_level(10)[0] == "LOW WATER ALERT"


def test_overflow_risk():
    assert classify_level(95)[0] == "OVERFLOW RISK"


def test_invalid_level():
    try:
        classify_level(110)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_health_endpoint():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
