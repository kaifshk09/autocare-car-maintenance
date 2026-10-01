import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AutoCare" in response.data


def test_blank_form_values_are_handled(client):
    response = client.post(
        "/",
        data={
            "age": "",
            "mileage": "",
            "service": "",
            "usage": "Normal",
            "warning": "No",
            "condition": "Good",
            "fuel": "Petrol",
        },
    )
    assert response.status_code == 200
    assert b"Low Risk" in response.data or b"Medium Risk" in response.data or b"High Risk" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
