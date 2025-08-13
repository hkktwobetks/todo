import pytest
import app.domains.tasks.router as tasks_router


pytestmark = pytest.mark.asyncio


async def test_404_not_found_shape(client):
    r = await client.get("/tasks/999")
    assert r.status_code == 404
    assert r.json()["error"] == "not_found"
    assert "detail" in r.json()

async def test_422_validation_shape(client):
    r = await client.post("/tasks/", json={"title": "", "status": "todo"})
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "validation_error"
    assert isinstance(body["detail"], list) and len(body["detail"]) >= 1


async def test_500_unexpected_shape(client, monkeypatch):
    # get_task を故意に例外化して 500 を誘発
    def boom(*_, **__):
        raise RuntimeError("boom")

    monkeypatch.setattr(tasks_router, "get_task", boom)

    r = await client.get("/tasks/1")
    assert r.status_code == 500
    body = r.json()
    assert body["error"] == "internal_server_error"
    assert body["detail"] == "unexpected error"
