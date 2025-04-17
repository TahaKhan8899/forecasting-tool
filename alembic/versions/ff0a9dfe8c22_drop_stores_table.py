"""Drop stores table

Revision ID: ff0a9dfe8c22
Revises: e042a28d3a70
Create Date: 2025-04-16 20:00:31.707272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff0a9dfe8c22'
down_revision: Union[str, None] = 'e042a28d3a70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Drop the redundant 'stores' table and its indexes from the 'app' schema."""
    # ### Manually added commands ###
    # Drop indexes associated with the 'stores' table in the 'app' schema first
    op.drop_index('ix_stores_store_url', table_name='stores', schema='app')
    op.drop_index(op.f('ix_app_stores_store_url'), table_name='stores', schema='app')
    # Drop the 'stores' table from the 'app' schema
    op.drop_table('stores', schema='app')
    # ### end commands ###


def downgrade() -> None:
    """Downgrade schema: Recreate the 'stores' table and its indexes in the 'app' schema."""
    # ### Manually added commands to reverse the upgrade ###
    # Recreate the 'stores' table (copied from migration a4f9bd5ebef0)
    op.create_table('stores',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('store_url', sa.String(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='app'
    )
    # Recreate indexes (copied from migration a4f9bd5ebef0)
    op.create_index(op.f('ix_app_stores_store_url'), 'stores', ['store_url'], unique=True, schema='app')
    op.create_index('ix_stores_store_url', 'stores', ['store_url'], unique=False, schema='app') # Note: Original migration had a create/drop for this index name without schema, potentially an error there too, but we replicate the creation part for downgrade.
    # ### end commands ###
