"""initial schema

Revision ID: 1867d492e7ba
Revises: 6b2c91b735df
Create Date: 2026-02-03 18:56:59.479601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1867d492e7ba'
down_revision: Union[str, Sequence[str], None] = '6b2c91b735df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
