"""empty message

Revision ID: 70858431de6e
Revises: 542ac3d9aede
Create Date: 2024-04-17 18:47:01.798517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70858431de6e'
down_revision: Union[str, None] = '542ac3d9aede'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
