"""empty message

Revision ID: 74597e9704d4
Revises: 1702735c78cf
Create Date: 2020-12-10 00:10:37.896544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74597e9704d4'
down_revision = '1702735c78cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('downloaders',
    sa.Column('downloaded_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['downloaded_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('downloaded_id')
    )
    op.create_table('viewers',
    sa.Column('viewed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['viewed_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('viewed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('viewers')
    op.drop_table('downloaders')
    # ### end Alembic commands ###
