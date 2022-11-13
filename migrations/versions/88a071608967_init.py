"""init

Revision ID: 88a071608967
Revises: 
Create Date: 2022-11-14 02:18:11.938095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '88a071608967'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dead_tokens',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('ext_id', sa.String(length=512), nullable=False),
                    sa.Column('token_value', sa.String(length=2048), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], use_alter=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('ext_id'),
                    sa.UniqueConstraint('token_value')
                    )
    op.create_table('items',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('entry_value', sa.String(length=128), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('rate', sa.Integer(), nullable=True),
                    sa.Column('carma', sa.Float(), nullable=True),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], use_alter=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('entry_value')
                    )
    op.create_table('users',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('display_name', sa.String(length=64), nullable=False),
                    sa.Column('user_name', sa.String(length=128), nullable=False),
                    sa.Column('ext_id', sa.String(length=512), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('ext_id'),
                    sa.UniqueConstraint('user_name')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('items')
    op.drop_table('dead_tokens')
    # ### end Alembic commands ###
