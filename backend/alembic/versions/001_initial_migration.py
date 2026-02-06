"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-02-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('industry', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('gstin', sa.String(length=15), nullable=True),
        sa.Column('pan', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registration_number')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)

    # Create financial_documents table
    op.create_table('financial_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(length=50), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_type', sa.String(length=10), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('processed', sa.Boolean(), nullable=True),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_financial_documents_company_id'), 'financial_documents', ['company_id'], unique=False)
    op.create_index(op.f('ix_financial_documents_id'), 'financial_documents', ['id'], unique=False)

    # Create financial_metrics table
    op.create_table('financial_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_revenue', sa.Float(), nullable=True),
        sa.Column('gross_profit', sa.Float(), nullable=True),
        sa.Column('net_profit', sa.Float(), nullable=True),
        sa.Column('operating_profit', sa.Float(), nullable=True),
        sa.Column('ebitda', sa.Float(), nullable=True),
        sa.Column('current_ratio', sa.Float(), nullable=True),
        sa.Column('quick_ratio', sa.Float(), nullable=True),
        sa.Column('cash_ratio', sa.Float(), nullable=True),
        sa.Column('gross_profit_margin', sa.Float(), nullable=True),
        sa.Column('net_profit_margin', sa.Float(), nullable=True),
        sa.Column('return_on_assets', sa.Float(), nullable=True),
        sa.Column('return_on_equity', sa.Float(), nullable=True),
        sa.Column('debt_to_equity', sa.Float(), nullable=True),
        sa.Column('debt_to_assets', sa.Float(), nullable=True),
        sa.Column('interest_coverage', sa.Float(), nullable=True),
        sa.Column('asset_turnover', sa.Float(), nullable=True),
        sa.Column('inventory_turnover', sa.Float(), nullable=True),
        sa.Column('receivables_turnover', sa.Float(), nullable=True),
        sa.Column('operating_cash_flow', sa.Float(), nullable=True),
        sa.Column('investing_cash_flow', sa.Float(), nullable=True),
        sa.Column('financing_cash_flow', sa.Float(), nullable=True),
        sa.Column('free_cash_flow', sa.Float(), nullable=True),
        sa.Column('working_capital', sa.Float(), nullable=True),
        sa.Column('accounts_receivable', sa.Float(), nullable=True),
        sa.Column('accounts_payable', sa.Float(), nullable=True),
        sa.Column('inventory', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_financial_metrics_company_id'), 'financial_metrics', ['company_id'], unique=False)
    op.create_index(op.f('ix_financial_metrics_id'), 'financial_metrics', ['id'], unique=False)

    # Create credit_scores table
    op.create_table('credit_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('rating', sa.String(length=5), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=True),
        sa.Column('factors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_scores_company_id'), 'credit_scores', ['company_id'], unique=False)
    op.create_index(op.f('ix_credit_scores_id'), 'credit_scores', ['id'], unique=False)

    # Create assessments table
    op.create_table('assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('financial_health_score', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=True),
        sa.Column('strengths', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('weaknesses', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('opportunities', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('threats', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('cost_optimization', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('revenue_enhancement', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('working_capital_tips', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tax_optimization', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('recommended_products', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('revenue_forecast', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('cash_flow_forecast', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('industry_benchmark', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('executive_summary', sa.Text(), nullable=True),
        sa.Column('detailed_analysis', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessments_company_id'), 'assessments', ['company_id'], unique=False)
    op.create_index(op.f('ix_assessments_id'), 'assessments', ['id'], unique=False)

    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=True),
        sa.Column('details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_company_id'), 'audit_logs', ['company_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_company_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_assessments_id'), table_name='assessments')
    op.drop_index(op.f('ix_assessments_company_id'), table_name='assessments')
    op.drop_table('assessments')
    op.drop_index(op.f('ix_credit_scores_id'), table_name='credit_scores')
    op.drop_index(op.f('ix_credit_scores_company_id'), table_name='credit_scores')
    op.drop_table('credit_scores')
    op.drop_index(op.f('ix_financial_metrics_id'), table_name='financial_metrics')
    op.drop_index(op.f('ix_financial_metrics_company_id'), table_name='financial_metrics')
    op.drop_table('financial_metrics')
    op.drop_index(op.f('ix_financial_documents_id'), table_name='financial_documents')
    op.drop_index(op.f('ix_financial_documents_company_id'), table_name='financial_documents')
    op.drop_table('financial_documents')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
