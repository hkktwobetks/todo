# tests/unit/test_tasks_schemas.py
import pytest
from pydantic import ValidationError
from app.domains.tasks.schemas import TaskCreate, TaskUpdate

def test_task_create_title_length_bounds():
    with pytest.raises(ValidationError):
        TaskCreate(title="", status="todo")
    TaskCreate(title="a", status="todo")            # OK
    TaskCreate(title="x"*100, status="todo")        # OK
    with pytest.raises(ValidationError):
        TaskCreate(title="x"*101, status="todo")    # 101はNG

def test_task_create_status_regex_validation():
    TaskCreate(title="a", status="todo")
    TaskCreate(title="a", status="in_progress")
    TaskCreate(title="a", status="done")
    with pytest.raises(ValidationError):
        TaskCreate(title="a", status="doing")       # 不正値
