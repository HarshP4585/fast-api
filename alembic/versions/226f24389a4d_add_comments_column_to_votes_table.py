"""add comments column to votes table

Revision ID: 226f24389a4d
Revises: 
Create Date: 2023-05-22 18:39:50.807434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '226f24389a4d'
# downgrade to previous version, Alembic maintains version history in the Database
down_revision = None
branch_labels = None
depends_on = None

# Doc: https://alembic.sqlalchemy.org/en/latest/api/index.html

def upgrade() -> None:
    """
        Update the database ie. drop, update, create table etc.
    """
    op.add_column("votes", sa.Column("comment", sa.String, nullable=True))


def downgrade() -> None:
    """
        Rollback steps if upgrade fails ie. create, revert, drop table etc.
    """
    op.drop_column("votes", "comment")
