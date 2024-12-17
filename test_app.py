import pytest
from app import app, is_sanitized

def test_is_sanitized():
    assert is_sanitized("normalInput") == True
    assert is_sanitized("SELECT * FROM users;") == False
    assert is_sanitized("DROP TABLE") == False
    assert is_sanitized("hello") == True
    assert is_sanitized("OR 1=1") == False

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sanitize_input(client):
    response=client.post('/v1/sanitized/input/', json={"payload":"hello"})
    assert response.get_json() == {"result": "sanitized"}

    response=client.post('/v1/sanitized/input/', json={"payload":"DROP Table;"})
    assert response.get_json() == {"result": "unsanitized"}

    response=client.post('/v1/sanitized/input/', json={"payload":"Hello"})
    assert response.get_json() == {"result": "sanitized"}

    response=client.post('/v1/sanitized/input/', json={"payload":"SELECT * FROM users;"})
    assert response.get_json() == {"result": "unsanitized"}
