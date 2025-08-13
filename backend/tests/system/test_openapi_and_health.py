# tests/system/test_openapi_and_health.py
import pytest
pytestmark = pytest.mark.asyncio

async def test_healthz_is_200(client):
    r = await client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

async def test_openapi_has_tasks_paths(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    paths = spec.get("paths", {})
    assert "/tasks/" in paths
    assert "/tasks/{task_id}" in paths
    # 代表的なSchema名が存在するか（例：TaskRead）
    comp = spec.get("components", {}).get("schemas", {})
    assert any("TaskRead" in key for key in comp.keys())
