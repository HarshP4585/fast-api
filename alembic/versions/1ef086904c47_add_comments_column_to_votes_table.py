"""add comments column to votes table

Revision ID: 1ef086904c47
Revises: 
Create Date: 2023-05-23 14:28:32.418652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ef086904c47'
down_revision = None
branch_labels = None
depends_on = None

# alembic revision --autogenerate -m "add comments column to votes table"
# -> sync changes from Models and create migration changes in the db, which can be executed by upgrading to the verison

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('comment', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('votes', 'comment')
    # ### end Alembic commands ###
