"""initial migration

Revision ID: 4d6274588458
Revises: 
Create Date: 2025-01-20 12:20:28.789004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d6274588458'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('digests',
    sa.Column('digest_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_sent', sa.DateTime(), nullable=True),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('digest_id')
    )
    op.create_table('newsletters',
    sa.Column('newsletter_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('date_received', sa.DateTime(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('newsletter_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('newsletters')
    op.drop_table('digests')
    op.drop_table('users')
    # ### end Alembic commands ###
