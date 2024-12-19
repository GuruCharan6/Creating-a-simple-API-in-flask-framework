import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sanitized_input_valid(client):
    response = client.post('/v1/sanitized/input/', json={"payload": "HelloWorld"})
    assert response.status_code == 200
    assert response.get_json() == {"result": "sanitized"}

def test_sanitized_input_sql_injection(client):
    sql_payloads = [
        "1=1",
        "' OR '1'='1",
        "SELECT * FROM users",
        "DROP TABLE users;",
        "UNION SELECT username, password FROM users",
        "admin' --"
    ]

    for payload in sql_payloads:
        response = client.post('/v1/sanitized/input/', json={"payload": payload})
        assert response.status_code == 200
        assert response.get_json() == {"result": "unsanitized"}

def test_sanitized_input_invalid_payload_type(client):
    response = client.post('/v1/sanitized/input/', json={"payload": 12345})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input, payload must be a string"}

def test_sanitized_input_empty_payload(client):
    response = client.post('/v1/sanitized/input/', json={"payload": ""})
    assert response.status_code == 200
    assert response.get_json() == {"result": "unsanitized"}

def test_sanitized_input_missing_payload(client):
    response = client.post('/v1/sanitized/input/', json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing payload"}

def test_sanitized_input_malformed_json(client):
    response = client.post('/v1/sanitized/input/', data="Not a JSON")
    assert response.status_code == 500
    assert "error" in response.get_json()

def test_sanitized_input_special_characters(client):
    special_characters = "<>!@#$%^&*()"
    response = client.post('/v1/sanitized/input/', json={"payload": special_characters})
    assert response.status_code == 200
    assert response.get_json() == {"result": "unsanitized"}
