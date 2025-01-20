"""add system user

Revision ID: system_user_001
Revises: 4d6274588458
Create Date: 2025-01-20 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'system_user_001'
down_revision = '4d6274588458'
branch_labels = None
depends_on = None

def upgrade():
    # Insert system user with current timestamp
    op.execute(
        "INSERT INTO users (email, password_hash, created_at) "
        "VALUES ('system@newsletter-aggregator.com', 'not_used_for_system_user', CURRENT_TIMESTAMP) "
        "ON CONFLICT (email) DO NOTHING"
    )

def downgrade():
    # Remove system user
    op.execute(
        "DELETE FROM users WHERE email = 'system@newsletter-aggregator.com'"
    ) 