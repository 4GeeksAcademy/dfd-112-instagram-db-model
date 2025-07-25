"""empty message

Revision ID: 5613de29c38a
Revises: 63d350c03635
Create Date: 2025-07-25 18:51:44.983023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5613de29c38a'
down_revision = '63d350c03635'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.Enum('IMAGE', 'VIDEO', name='mediatype'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
