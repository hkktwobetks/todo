"""create tasks table

Revision ID: 2cd3df0ae252
Revises: 1f19994c3362
Create Date: 2025-08-09 13:28:36.101445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cd3df0ae252'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_tasks_status", "tasks", ["status"])
    op.create_index("idx_tasks_due_at", "tasks", ["due_at"])
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"])


def downgrade():
    op.drop_index("idx_tasks_created_at", table_name="tasks")
    op.drop_index("idx_tasks_due_at", table_name="tasks")
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_table("tasks")