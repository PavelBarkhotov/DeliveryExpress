"""Создание типов посылок

Revision ID: 799abda56fff
Revises: 0aec2c4ca7c6
Create Date: 2026-08-16 01:36:51.412096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '799abda56fff'
down_revision: Union[str, Sequence[str], None] = '0aec2c4ca7c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

parcel_types = sa.table(
    "parcel_types",
    sa.column("name", sa.String),
)

def upgrade() -> None:
    op.bulk_insert(parcel_types,
                   [
                       {"name": "Одежда"},
                       {"name": "Электроника"},
                       {"name": "Разное"}
                   ])


def downgrade() -> None:
    op.execute(
        parcel_types.delete().where(
            parcel_types.c.name.in_(
                ["Одежда","Электроника", "Разное"]
            )
        )
    )
