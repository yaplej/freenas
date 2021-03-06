"""Complete filesystem replicate option

Revision ID: 8b5d36242d44
Revises: 7e8f7f07153e
Create Date: 2019-11-08 19:36:27.373757+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b5d36242d44'
down_revision = '7e8f7f07153e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repl_replicate', sa.Boolean(), nullable=True))

    op.execute("UPDATE storage_replication SET repl_replicate = 0")

    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.alter_column('repl_replicate',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.drop_column('repl_replicate')
    # ### end Alembic commands ###
