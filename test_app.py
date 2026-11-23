import pytest
from app import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    return create_app().test_client()


def test_health(client):
    assert client.get("/health").json == {"status": "ok"}


def test_add_and_list(client):
    assert client.post("/items", json={"name": "vis", "quantity": 10}).status_code == 201
    assert client.get("/items").json[0]["name"] == "vis"
    assert client.get("/items").json[0]["quantity"] == 10


@pytest.mark.parametrize("payload", [
    {}, {"name": "", "quantity": 1}, {"name": "x", "quantity": -1},
    {"name": "x", "quantity": "1"}, {"name": 5, "quantity": 1},
])
def test_validation(client, payload):
    assert client.post("/items", json=payload).status_code == 400


def test_sql_injection_is_inert(client):
    evil = "x'); DROP TABLE items;--"
    assert client.post("/items", json={"name": evil, "quantity": 1}).status_code == 201
    assert client.get("/items").json[0]["name"] == evil
