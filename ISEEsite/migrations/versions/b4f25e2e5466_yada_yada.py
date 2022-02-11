"""yada yada

Revision ID: b4f25e2e5466
Revises: 6f3b44fb6f4b
Create Date: 2021-10-06 17:14:34.703887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4f25e2e5466'
down_revision = '6f3b44fb6f4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    op.add_column('students', sa.Column('wordlist', sa.String(length=128), nullable=True))
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_column('students', 'wordlist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('wordlist_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'students', 'words', ['wordlist_id'], ['id'])
    op.drop_column('students', 'wordlist')
    op.create_table('words',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
