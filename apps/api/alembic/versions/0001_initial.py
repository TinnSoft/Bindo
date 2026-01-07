"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-01-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'workspaces',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
    )

    op.create_table(
        'requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('workspace_id', sa.Integer(), sa.ForeignKey('workspaces.id')),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('company_name', sa.String(length=255)),
        sa.Column('nit', sa.String(length=64)),
        sa.Column('contract_value', sa.Float()),
        sa.Column('term_months', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('request_id', sa.Integer(), sa.ForeignKey('requests.id')),
        sa.Column('path', sa.String(length=1024)),
        sa.Column('pages', sa.Integer()),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'extracted_fields',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('request_id', sa.Integer(), sa.ForeignKey('requests.id')),
        sa.Column('key', sa.String(length=255)),
        sa.Column('value', sa.Text()),
        sa.Column('confidence', sa.Float()),
        sa.Column('source', sa.String(length=32), server_default='llm'),
        sa.Column('evidence_page', sa.Integer()),
        sa.Column('evidence_text', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('workspace_id', sa.Integer(), sa.ForeignKey('workspaces.id')),
        sa.Column('request_id', sa.Integer(), sa.ForeignKey('requests.id')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(length=255)),
        sa.Column('field_key', sa.String(length=255)),
        sa.Column('before', sa.Text()),
        sa.Column('after', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('extracted_fields')
    op.drop_table('documents')
    op.drop_table('requests')
    op.drop_table('users')
    op.drop_table('workspaces')
