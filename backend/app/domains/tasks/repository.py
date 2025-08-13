from sqlalchemy import select,func, update as sa_update
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Task
from datetime import datetime
from .schemas import TaskCreate
from typing import Optional, Tuple , List

async def list_tasks(
    session: AsyncSession,
    status: Optional[str] = None,
    due_before: Optional[datetime] = None,
    *,
    limit: int = 20,
    offset: int = 0,
):
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    if due_before:
        stmt = stmt.where(Task.due_at <= due_before)

    stmt = stmt.order_by(Task.due_at.asc().nulls_last(), Task.id.asc()) \
               .limit(limit).offset(offset)

    res = await session.execute(stmt)
    return res.scalars().all()

async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    now = datetime.utcnow()
    task = Task(
        title=task_in.title,
        status=task_in.status,
        due_at=task_in.due_at,
        created_at=now,
        updated_at=now,
        completed_at=now if task_in.status == "done" else None,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    res = await session.execute(select(Task).where(Task.id == task_id))
    return res.scalars().first()

async def update_task_fields(session: AsyncSession, task_id: int, values: dict) -> Task | None:
    await session.execute(
        sa_update(Task)
        .where(Task.id == task_id)
        .values(**values)
    )
    await session.commit()
    return await get_task(session, task_id)

async def delete_task(session: AsyncSession, task_id: int) -> bool:
    res = await session.execute(sa_delete(Task).where(Task.id == task_id))
    if res.rowcount == 0:
        await session.rollback()
        return False
    await session.commit()
    return True

async def list_tasks_with_total(
        session: AsyncSession,
        status: Optional[str] = None,
        due_before: Optional[datetime] = None,
        *,
        limit: int = 20,
        offset: int = 0,
) -> Tuple[List[Task], int]:
    base = select(Task)
    if status:
        base = base.where(Task.status == status)
    if due_before:
        base = base.where(Task.due_at <= due_before)

    total_stmt = base.with_only_columns([func.count()]).order_by(None)
    total = await session.execute(total_stmt)

    items_stmt = (
        base.order_by(Task.due_at.asc().nulls_last(), Task.id.asc())
        .limit(limit)
        .offset(offset)
    )
    items = (await session.execute(items_stmt)).scalars().all()

    return items, total