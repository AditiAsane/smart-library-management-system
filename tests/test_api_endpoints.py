from app import create_app


def test_health_endpoint():
    client = create_app().test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_get_seeded_user():
    client = create_app().test_client()
    response = client.get("/api/users/U101")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Alice Johnson"


def test_get_books():
    client = create_app().test_client()
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.get_json()) >= 2


def test_missing_user_returns_404():
    client = create_app().test_client()
    response = client.get("/api/users/UNKNOWN")
    assert response.status_code == 404
