"""adding new operations

Revision ID: 8cdc063783b2
Revises: af9a23125b82
Create Date: 2025-02-15 02:30:45.128602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from db.schemas import OPERATION_VALUES

# revision identifiers, used by Alembic.
revision: str = '8cdc063783b2'
down_revision: Union[str, None] = 'af9a23125b82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    new_enum = ", ".join([f"'{x}'" for x in OPERATION_VALUES.keys()])
    
    op.execute('alter type typeoperations rename to typeoperations_temp')
    op.execute(f"create type typeoperations as enum ({new_enum})")
    op.execute('alter table ledger rename column operation to operation_temp')
    op.execute('alter table ledger add operation typeoperations')
    op.execute('update ledger set operation = operation_temp::text::typeoperations')
    op.execute('alter table ledger drop column operation_temp')
    op.execute('drop type typeoperations_temp')
    # ### end Alembic commands ###



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter type typeoperations rename to typeoperations_temp')
    op.execute("create type typeoperations as enum ('DAILY_REWARD', 'SIGNUP_CREDIT', 'CREDIT_SPEND', 'CREDIT_ADD')")    
    op.execute('alter table ledger rename column operation to operation_temp')
    op.execute('alter table ledger add operation typeoperations')
    op.execute('update ledger set operation = operation_temp::text::typeoperations')
    op.execute('alter table ledger drop column operation_temp')
    op.execute('drop type typeoperations_temp')
    # ### end Alembic commands ###
