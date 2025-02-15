import sys
sys.path = ['', '..'] + sys.path[1:]

from core.ledgers.schemas import BaseLedgerOperation, SHARED_OPERATION_VALUES, SHARED_OPERATION_CONFIG

APP_OPERATION_CONFIG = {
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}

LEDGER_OPERATION_CONFIG = {**APP_OPERATION_CONFIG, **SHARED_OPERATION_CONFIG}

APP_OPERATION_VALUES = {
    "CONTENT_CREATION": "CONTENT_CREATION",
    "CONTENT_ACCESS": "CONTENT_ACCESS"
}

OPERATION_VALUES = {**APP_OPERATION_VALUES, **SHARED_OPERATION_VALUES}

LedgerOperation = BaseLedgerOperation("TypeOperations", OPERATION_VALUES)
