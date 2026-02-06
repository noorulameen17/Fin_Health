"""add executive summary and metadata to assessments

Revision ID: 002_add_assessment_fields
Revises: 001_initial_migration
Create Date: 2026-02-06

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_assessment_fields'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to assessments table
    op.add_column('assessments', sa.Column('executive_summary', sa.Text(), nullable=True))
    op.add_column('assessments', sa.Column('language', sa.String(length=10), nullable=True, server_default='en'))
    op.add_column('assessments', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True))
    op.add_column('assessments', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove the columns if rolling back
    op.drop_column('assessments', 'updated_at')
    op.drop_column('assessments', 'created_at')
    op.drop_column('assessments', 'language')
    op.drop_column('assessments', 'executive_summary')
