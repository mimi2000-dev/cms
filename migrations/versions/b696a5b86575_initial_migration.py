"""Initial migration

Revision ID: b696a5b86575
Revises: 
Create Date: 2024-08-20 11:25:43.687239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b696a5b86575'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=8), nullable=True),
    sa.Column('role', sa.Enum('client', 'admin', name='userstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('updated', sa.Date(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_request_form',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('reason', sa.String(length=100), nullable=False),
    sa.Column('updated', sa.Date(), nullable=True),
    sa.Column('client', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('nrc_number', sa.String(length=15), nullable=True),
    sa.Column('district', sa.String(length=200), nullable=False),
    sa.Column('pdf_file', sa.LargeBinary(), nullable=True),
    sa.Column('file_name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client'], ['user.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nrc_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_request_form')
    op.drop_table('service')
    op.drop_table('user')
    # ### end Alembic commands ###
