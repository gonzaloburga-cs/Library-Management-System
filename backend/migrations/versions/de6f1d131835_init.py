"""init

Revision ID: de6f1d131835
Revises: 
Create Date: 2025-09-11 21:22:26.347568

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de6f1d131835'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table(
        'books',
        sa.Column('id', sa.UUID, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('author', sa.Text, nullable=False),
        sa.Column('isbn', sa.Text, nullable=False),
        sa.Column('is_checked_out', sa.Boolean, server_default=sa.text("false"), nullable=False)
    )
    op.create_table(
        'users',
        sa.Column('id', sa.UUID, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('supabase_id', sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text("now()"), nullable=False)
    )
    op.create_table(
        'checkout_logs',
        sa.Column('id', sa.UUID, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('checkout_date', sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column('checkin_date', sa.DateTime, nullable=True),
        sa.Column('book_id', sa.UUID, sa.ForeignKey('books.id'), nullable=False),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('users.id'), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('checkout_logs')
    op.drop_table('users')
    op.drop_table('books')
