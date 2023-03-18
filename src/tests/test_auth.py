def test_correct_register(client):
    request = {
        "full_name": "Pytest User 2",
        "email": "pytest@email.com",
        "password": "pytester",
    }
    response = client.post("/auth/register", json=request)
    assert response.status_code == 200
    assert response.get_json()["token"]


def test_incorrect_register_email(client):
    request = {
        "full_name": "Pytest User 2",
        "email": "",
        "password": "pytester",
    }
    response = client.post("/auth/register", json=request)
    assert response.status_code == 400
    assert "email" in response.get_json()["error"]


def test_incorrect_register_password(client):
    request = {
        "full_name": "Pytest User 2",
        "email": "pytest@email.com",
        "password": "",
    }
    response = client.post("/auth/register", json=request)
    assert response.status_code == 400
    assert "password" in response.get_json()["error"]


def test_correct_login(client):
    request = {
        "email": "test_user@email.com",
        "password": "usseerr",
    }
    response = client.post("/auth/login", json=request)
    assert response.status_code == 200
    assert response.get_json()["token"]


def test_incorrect_login_short(client):
    request = {
        "email": "test_user@email.com",
        "password": "user",
    }
    response = client.post("/auth/login", json=request)
    assert response.status_code == 401
    assert "password" in response.get_json()["error"]


def test_incorrect_login_wrong(client):
    request = {
        "email": "test_user@email.com",
        "password": "this_is_wrong",
    }
    response = client.post("/auth/login", json=request)
    assert response.status_code == 401
    assert "password" in response.get_json()["error"]
