"""Initial task table

Revision ID: 001
Revises:
Create Date: 2025-12-16 18:57:38.202105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])
    op.create_index('ix_tasks_completed_created_at', 'tasks', ['completed', 'created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_tasks_completed_created_at', table_name='tasks')
    op.drop_index('ix_tasks_completed', table_name='tasks')

    # Drop the tasks table
    op.drop_table('tasks')