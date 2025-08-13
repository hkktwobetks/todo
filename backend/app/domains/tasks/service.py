from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import get_task, update_task_fields
from .schemas import TaskUpdate

async def update_task(session: AsyncSession, task_id: int, data: TaskUpdate):
    row = await get_task(session, task_id)
    if not row:
        return None  # 404はrouterで返す

    now = datetime.now(timezone.utc)

    values: dict = {"updated_at": now}

    if data.title is not None:
        values["title"] = data.title
    if data.due_at is not None:
        values["due_at"] = data.due_at
    if data.status is not None:
        values["status"] = data.status
        # 業務ルール：doneならcompleted_atを埋める／それ以外はNULL
        values["completed_at"] = now if data.status == "done" else None

    return await update_task_fields(session, task_id, values)
