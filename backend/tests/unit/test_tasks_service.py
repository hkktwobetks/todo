# tests/unit/test_tasks_service.py
import types
import pytest
from datetime import datetime, timezone
from app.domains.tasks import service as svc

pytestmark = pytest.mark.asyncio

class DummyTask:
    def __init__(self, **kw): self.__dict__.update(kw)

class DummySession: pass

async def test_update_status_to_done_sets_completed_at_now(monkeypatch):
    # 固定時刻
    fixed = datetime(2025, 8, 9, 0, 0, 0, tzinfo=timezone.utc)
    fake_dt = types.SimpleNamespace(now=lambda tz=None: fixed)

    # 既存レコード
    existing = DummyTask(id=1, title="A", status="todo", completed_at=None, updated_at=fixed)

    async def fake_get(_session, _id): return existing
    async def fake_update(_s, _id, values):
        # ここで期待値をざっくり検証
        assert values["status"] == "done"
        assert values["completed_at"] == fixed
        assert values["updated_at"] == fixed
        return DummyTask(id=1, title="A", **values)

    monkeypatch.setattr(svc, "get_task", fake_get)
    monkeypatch.setattr(svc, "update_task_fields", fake_update)
    monkeypatch.setattr(svc, "datetime", fake_dt)  # serviceモジュール内のdatetimeを差し替え

    out = await svc.update_task(DummySession(), 1, types.SimpleNamespace(title=None, status="done", due_at=None))
    assert out.status == "done"
    assert out.completed_at == fixed

async def test_update_status_from_done_to_in_progress_clears_completed_at(monkeypatch):
    fixed = datetime(2025, 8, 9, 0, 0, 0, tzinfo=timezone.utc)
    fake_dt = types.SimpleNamespace(now=lambda tz=None: fixed)

    existing = DummyTask(id=1, title="A", status="done", completed_at=fixed, updated_at=fixed)

    async def fake_get(_session, _id): return existing
    async def fake_update(_s, _id, values):
        assert values["status"] == "in_progress"
        assert values["completed_at"] is None
        return DummyTask(id=1, title="A", **values)

    monkeypatch.setattr(svc, "get_task", fake_get)
    monkeypatch.setattr(svc, "update_task_fields", fake_update)
    monkeypatch.setattr(svc, "datetime", fake_dt)

    out = await svc.update_task(DummySession(), 1, types.SimpleNamespace(title=None, status="in_progress", due_at=None))
    assert out.status == "in_progress"
    assert out.completed_at is None
