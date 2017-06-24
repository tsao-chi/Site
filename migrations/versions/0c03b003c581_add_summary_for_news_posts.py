"""Add summary for news posts

Revision ID: 0c03b003c581
Revises: 1eb82ac2fee5
Create Date: 2017-06-24 19:45:44.395376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c03b003c581'
down_revision = '1eb82ac2fee5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news_post', sa.Column('summary', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news_post', 'summary')
    # ### end Alembic commands ###
