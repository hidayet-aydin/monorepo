import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Sequence, Enum, DateTime

from .schemas import LedgerOperation


class Base(DeclarativeBase):
    pass


class Ledger(Base):
    __tablename__ = 'ledger'
    id = Column(Integer, Sequence('ledger_id_seq'), primary_key=True)
    operation = Column(Enum(LedgerOperation))
    amount = Column(Integer)
    nonce = Column(String(50))
    owner_id = Column(String(50))
    created_on = Column(DateTime, default=datetime.datetime.now)
