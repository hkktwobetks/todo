from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from .schemas import TaskRead, TaskCreate, TaskUpdate, TaskPage
from .service import update_task as svc_update_task
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.shared.exceptions import NotFound


from app.core.db import get_session
from .repository import list_tasks, create_task, get_task
from .repository import delete_task as repo_delete_task
from .repository import list_tasks_with_total
from .schemas import TaskPage
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    status: Optional[str] = Query(None, pattern="^(todo|in_progress|done)$"),
    due_before: Optional[datetime] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    rows = await list_tasks(session, status, due_before, limit=limit, offset=offset)
    return rows


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    row = await get_task(session, task_id)
    if row is None:
        raise NotFound("Task not found")
    return row


@router.post("/", response_model=TaskRead, status_code=201)
async def create_new_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    task = await create_task(session, task_in)
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    session: AsyncSession = Depends(get_session),
):
    row = await svc_update_task(session, task_id, payload)
    if row is None:
        raise NotFound("Task not found")
    return row

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    success = await repo_delete_task(session, task_id)
    if not success:
        raise NotFound("Task not found")
    return Response(status_code=204)  # No Content


@router.get("/", response_model=TaskPage)
async def get_tasks(
    status: Optional[str] = Query(None, pattern="^(todo|in_progress|done)$"),
    due_before: Optional[datetime] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    items, total = await list_tasks_with_total(
        session, status, due_before, limit=limit, offset=offset
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}
