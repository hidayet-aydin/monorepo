from sqlalchemy.orm import Session

from .models import Ledger
from .schemas import LEDGER_OPERATION_CONFIG


class NotFoundError(Exception):
    pass


def db_read_user_last_operation(user_id: str, db: Session):
    result = db.query(Ledger).filter_by(
        owner_id=user_id).order_by(Ledger.id.desc()).first()

    if result is None:
        raise NotFoundError(f"User {user_id} not found in the database.")
    return result


def db_insert_ledger(ledger: Ledger, db: Session):
    db.add(ledger)
    db.commit()
