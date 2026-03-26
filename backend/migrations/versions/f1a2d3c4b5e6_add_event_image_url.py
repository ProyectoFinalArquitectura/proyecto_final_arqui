"""add optional event image_url

Revision ID: f1a2d3c4b5e6
Revises: 8456c81c2a36
Create Date: 2026-03-26 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1a2d3c4b5e6"
down_revision = "8456c81c2a36"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("events", sa.Column("image_url", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("events", "image_url")
