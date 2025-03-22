"""Initial migration

Revision ID: 20240322_initial
Revises: 
Create Date: 2024-03-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20240322_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE modelprovider AS ENUM ('openai', 'anthropic', 'google', 'huggingface', 'local')")
    op.execute("CREATE TYPE evaluationtype AS ENUM ('factual_qa', 'reasoning', 'coding', 'math', 'safety', 'jailbreak', 'agent')")
    
    # Create models table
    op.create_table(
        'models',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('provider', postgresql.ENUM('openai', 'anthropic', 'google', 'huggingface', 'local', name='modelprovider'), nullable=False),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parameters', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create prompts table
    op.create_table(
        'prompts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('type', postgresql.ENUM('factual_qa', 'reasoning', 'coding', 'math', 'safety', 'jailbreak', 'agent', name='evaluationtype'), nullable=False),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create evaluations table
    op.create_table(
        'evaluations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('model_id', sa.String(), nullable=False),
        sa.Column('prompt_id', sa.String(), nullable=False),
        sa.Column('completion', sa.Text(), nullable=False),
        sa.Column('scores', postgresql.JSONB(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
        sa.ForeignKeyConstraint(['prompt_id'], ['prompts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create regression_logs table
    op.create_table(
        'regression_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('model_id', sa.String(), nullable=False),
        sa.Column('evaluation_type', postgresql.ENUM('factual_qa', 'reasoning', 'coding', 'math', 'safety', 'jailbreak', 'agent', name='evaluationtype'), nullable=False),
        sa.Column('previous_score', sa.Float(), nullable=True),
        sa.Column('current_score', sa.Float(), nullable=True),
        sa.Column('difference', sa.Float(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create failure_cases table
    op.create_table(
        'failure_cases',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('evaluation_id', sa.String(), nullable=False),
        sa.Column('failure_type', sa.String(), nullable=False),
        sa.Column('severity', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['evaluation_id'], ['evaluations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_models_provider'), 'models', ['provider'], unique=False)
    op.create_index(op.f('ix_prompts_type'), 'prompts', ['type'], unique=False)
    op.create_index(op.f('ix_evaluations_model_id'), 'evaluations', ['model_id'], unique=False)
    op.create_index(op.f('ix_evaluations_prompt_id'), 'evaluations', ['prompt_id'], unique=False)
    op.create_index(op.f('ix_regression_logs_model_id'), 'regression_logs', ['model_id'], unique=False)
    op.create_index(op.f('ix_failure_cases_evaluation_id'), 'failure_cases', ['evaluation_id'], unique=False)

def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_failure_cases_evaluation_id'), table_name='failure_cases')
    op.drop_index(op.f('ix_regression_logs_model_id'), table_name='regression_logs')
    op.drop_index(op.f('ix_evaluations_prompt_id'), table_name='evaluations')
    op.drop_index(op.f('ix_evaluations_model_id'), table_name='evaluations')
    op.drop_index(op.f('ix_prompts_type'), table_name='prompts')
    op.drop_index(op.f('ix_models_provider'), table_name='models')
    
    # Drop tables
    op.drop_table('failure_cases')
    op.drop_table('regression_logs')
    op.drop_table('evaluations')
    op.drop_table('prompts')
    op.drop_table('models')
    
    # Drop enum types
    op.execute('DROP TYPE evaluationtype')
    op.execute('DROP TYPE modelprovider') 