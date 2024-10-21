"""some chan

Revision ID: 542ac3d9aede
Revises: 79751676a8b6
Create Date: 2024-04-17 18:45:15.370292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '542ac3d9aede'
down_revision: Union[str, None] = '79751676a8b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
