"""stuff added in file model

Revision ID: 6ec29c8de008
Revises: 9e6e9553112f
Create Date: 2023-03-01 21:08:20.497228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ec29c8de008'
down_revision = '9e6e9553112f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expires_in', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.drop_column('expires_in')

    # ### end Alembic commands ###