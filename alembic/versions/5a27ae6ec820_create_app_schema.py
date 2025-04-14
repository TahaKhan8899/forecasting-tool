"""Create app schema

Revision ID: 5a27ae6ec820
Revises: 5856d47e5369
Create Date: 2025-04-14 18:24:51.108569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a27ae6ec820'
down_revision: Union[str, None] = '5856d47e5369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS app")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS app CASCADE")
