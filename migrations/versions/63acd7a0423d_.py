"""empty message

Revision ID: 63acd7a0423d
Revises: 
Create Date: 2021-10-06 10:50:30.650278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63acd7a0423d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Disaster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('EventTitle', sa.String(length=150), nullable=True),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('Location', sa.String(length=200), nullable=True),
    sa.Column('Pictures', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('Latitude', sa.String(), nullable=True),
    sa.Column('Longitude', sa.FLOAT(), nullable=True),
    sa.Column('Category', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Disaster')
    # ### end Alembic commands ###