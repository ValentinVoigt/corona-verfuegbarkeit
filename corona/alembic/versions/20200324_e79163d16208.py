"""User.last_invite

Revision ID: e79163d16208
Revises: 1a25a9b2fc1b
Create Date: 2020-03-24 18:33:34.373465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e79163d16208'
down_revision = '1a25a9b2fc1b'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_invite', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_invite')
    # ### end Alembic commands ###
