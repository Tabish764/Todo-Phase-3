"""Add conversation tables

Revision ID: 007_add_conversation_tables
Revises:
Create Date: 2025-12-26 22:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '007_add_conversation_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for user_id
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])

    # Create index for updated_at
    op.create_index('ix_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for conversation_id
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])

    # Create index for created_at
    op.create_index('ix_messages_created_at', 'messages', ['created_at'])

    # Create index for user_id
    op.create_index('ix_messages_user_id', 'messages', ['user_id'])

    # Add check constraint for role column
    op.create_check_constraint(
        'valid_role_check',
        'messages',
        'role IN (\'user\', \'assistant\', \'system\')'
    )


def downgrade() -> None:
    # Drop check constraint first
    op.drop_constraint('valid_role_check', 'messages', type_='check')

    # Drop indexes
    op.drop_index('ix_messages_user_id', table_name='messages')
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_index('ix_conversations_updated_at', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')

    # Drop messages table
    op.drop_table('messages')

    # Drop conversations table
    op.drop_table('conversations')