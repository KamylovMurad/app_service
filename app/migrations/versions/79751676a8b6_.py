"""empty message

Revision ID: 79751676a8b6
Revises: 63d280331cf8
Create Date: 2024-04-17 18:43:45.885977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79751676a8b6'
down_revision: Union[str, None] = '63d280331cf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
