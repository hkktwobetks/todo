# tests/integration/test_tasks_api.py
import pytest
pytestmark = pytest.mark.asyncio

async def test_create_then_list_returns_item(client):
    r = await client.post("/tasks/", json={"title": "A", "status": "todo"})
    assert r.status_code == 201
    r = await client.get("/tasks/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1 and items[0]["title"] == "A"

async def test_list_filters_by_status(client):
    await client.post("/tasks/", json={"title": "A", "status": "todo"})
    await client.post("/tasks/", json={"title": "B", "status": "done"})
    r = await client.get("/tasks/?status=todo")
    assert r.status_code == 200
    items = [x["status"] for x in r.json()]
    assert set(items) == {"todo"}

async def test_list_filters_by_due_before(client):
    await client.post("/tasks/", json={"title": "A", "status": "todo", "due_at": "2025-08-09T00:00:00Z"})
    await client.post("/tasks/", json={"title": "B", "status": "todo", "due_at": "2025-08-10T00:00:00Z"})
    await client.post("/tasks/", json={"title": "C", "status": "todo", "due_at": "2025-08-11T00:00:00Z"})
    r = await client.get("/tasks/?due_before=2025-08-10T00:00:00Z")
    items = r.json()
    # 8/9 と 8/10 がヒット（並び: due_at ASC, id ASC）
    assert [it["title"] for it in items] == ["A", "B"]

async def test_pagination_limit_offset(client):
    for i in range(6):
        await client.post("/tasks/", json={"title": f"T{i+1}", "status": "todo"})
    r = await client.get("/tasks/?limit=2&offset=2")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    # 既定ソート: due_at NULLS LAST, id ASC → 作成順で3,4件目が来る
    assert [it["title"] for it in items] == ["T3", "T4"]

async def test_update_status_toggles_completed_at(client):
    await client.post("/tasks/", json={"title": "A", "status": "todo"})
    r = await client.put("/tasks/1", json={"status": "done"})
    body = r.json()
    assert r.status_code == 200 and body["status"] == "done" and body["completed_at"] is not None
    r = await client.put("/tasks/1", json={"status": "in_progress"})
    body = r.json()
    assert r.status_code == 200 and body["status"] == "in_progress" and body["completed_at"] is None

async def test_delete_then_second_delete_is_404(client):
    await client.post("/tasks/", json={"title": "X", "status": "todo"})
    r = await client.delete("/tasks/1")
    assert r.status_code == 204
    r = await client.delete("/tasks/1")
    assert r.status_code == 404
