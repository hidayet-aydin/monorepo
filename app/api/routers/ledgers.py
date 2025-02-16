
import datetime
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.init import get_db
from db.models import Ledger
from db.schemas import LedgerOperation, LEDGER_OPERATION_CONFIG
from db.operations import NotFoundError, db_read_user_last_operation, db_insert_ledger


router = APIRouter()


class PayloadType(BaseModel):
    operation: LedgerOperation
    nonce: str
    owner_id: str


@router.get("/ledger/{owner_id}")
async def ledger_user_status(owner_id: str, response: Response, db: Session = Depends(get_db)):
    try:
        # get the last ledger operation for the user
        result = db_read_user_last_operation(owner_id, db)
    except NotFoundError:
        # return not-found message if the user not exists
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": 404,
            "desc": "not-found",
            "msg": "User not found!",
            "nonce": datetime.datetime.now().isoformat()
        }

    response.status_code = status.HTTP_200_OK
    return {"owner_id": owner_id, "amount": result.amount}


@router.post("/ledger")
def ledger_operation(payload: PayloadType, response: Response, db: Session = Depends(get_db)):
    try:
        # get the last ledger operation for the user
        result = db_read_user_last_operation(payload.owner_id, db)
    except NotFoundError:
        # return not-found message if the user not exists and operation is not signup credit
        if payload.operation.value != "SIGNUP_CREDIT":
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": 404,
                "desc": "not-found",
                "msg": "User not found!",
                "nonce": datetime.datetime.now().isoformat()
            }

    # return conflict message if the user exists and operation is same as previous one
    if result.operation.value == payload.operation.value and result.owner_id == payload.owner_id and result.nonce == payload.nonce:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "status": 409,
            "desc": "conflict",
            "msg": "Ledger operation is already done!",
            "nonce": datetime.datetime.now().isoformat()
        }

    # calculate the requested amount and previous ledger amount
    operation_calc = LEDGER_OPERATION_CONFIG[payload.operation.value]
    amount = 0 if result is None else result.amount
    new_amount = amount + operation_calc

    if new_amount < 0:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {
            "status": 406,
            "desc": "not-acceptable",
            "msg": "Not enought credit!",
            "nonce": datetime.datetime.now().isoformat()
        }

    ledger = Ledger(
        operation=payload.operation,
        amount=new_amount,
        owner_id=payload.owner_id if result is None else result.owner_id,
        nonce=payload.nonce,
    )
    db_insert_ledger(ledger, db)

    response.status_code = status.HTTP_201_CREATED
    return {
        "status": 201,
        "desc": "created",
        "msg": "Ledger operation succesfully completed!",
        "nonce": datetime.datetime.now().isoformat()
    }
