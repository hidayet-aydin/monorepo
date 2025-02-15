import sys
import datetime
from pathlib import Path

parent_path = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(parent_path)


import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from db.init import get_db
from db.schemas import LedgerOperation
from dependencies import get_token_header


client = TestClient(app)
mock_db = MagicMock(spec=Session)


def override_get_db():
    try:
        yield mock_db
    finally:
        pass


def override_get_token_header():
    pass


app.dependency_overrides[get_token_header] = override_get_token_header
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    return mock_db


def test_get_ledger_status_user_not_found(db):
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None

    response = client.get("/ledger/test_owner_id")

    assert response.status_code == 404
    resp_json = response.json()
    assert resp_json.get("status") == 404
    assert resp_json.get("desc") == "not-found"
    assert resp_json.get("msg") == "User not found!"


def test_get_ledger_status_user_found(db):
    mock_user = MagicMock()
    mock_user.owner_id = "test_owner_id"
    mock_user.amount = 10
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_user

    response = client.get("/ledger/test_owner_id")

    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json.get("owner_id") == "test_owner_id"
    assert resp_json.get("amount") == 10


def test_post_user_not_found_and_not_signed_up(db):
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None

    payload = {
        "operation": "DAILY_REWARD",
        "owner_id": "test_owner_id",
        "nonce": datetime.datetime.now().isoformat(),
    }
    response = client.post("/ledger", json=payload)

    assert response.status_code == 404
    resp_json = response.json()
    assert resp_json.get("status") == 404
    assert resp_json.get("desc") == "not-found"
    assert resp_json.get("msg") == "User not found!"


def test_post_avoid_duplicate_ledger_operations(db):
    nonce = datetime.datetime.now().isoformat()

    mock_user = MagicMock()
    operation_value = MagicMock()
    operation_value.value = LedgerOperation.DAILY_REWARD
    mock_user.operation = operation_value
    mock_user.owner_id = "test_owner_id"
    mock_user.nonce = nonce
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_user

    payload = {
        "operation": "DAILY_REWARD",
        "owner_id": "test_owner_id",
        "nonce": nonce,
    }
    response = client.post("/ledger", json=payload)

    assert response.status_code == 409
    resp_json = response.json()
    assert resp_json.get("status") == 409
    assert resp_json.get("desc") == "conflict"
    assert resp_json.get("msg") == "Ledger operation is already done!"


def test_post_not_enought_amount(db):
    mock_user = MagicMock()
    operation_value = MagicMock()
    operation_value.value = LedgerOperation.CREDIT_SPEND
    mock_user.operation = operation_value
    mock_user.owner_id = "test_owner_id"
    mock_user.nonce = datetime.datetime.now().isoformat()
    mock_user.amount = 0
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_user

    payload = {
        "operation": "CREDIT_SPEND",
        "owner_id": "test_owner_id",
        "nonce": datetime.datetime.now().isoformat(),
    }

    response = client.post("/ledger", json=payload)

    assert response.status_code == 406
    resp_json = response.json()
    assert resp_json.get("status") == 406
    assert resp_json.get("desc") == "not-acceptable"
    assert resp_json.get("msg") == "Not enought credit!"


def test_post_succesful_ledger_operation(db):
    mock_user = MagicMock()
    operation_value = MagicMock()
    operation_value.value = LedgerOperation.DAILY_REWARD
    mock_user.operation = operation_value
    mock_user.owner_id = "test_owner_id"
    mock_user.nonce = datetime.datetime.now().isoformat()
    mock_user.amount = 10
    db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_user

    payload = {
        "operation": "CREDIT_SPEND",
        "owner_id": "test_owner_id",
        "nonce": datetime.datetime.now().isoformat(),
    }
    response = client.post("/ledger", json=payload)

    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json.get("status") == 201
    assert resp_json.get("desc") == "created"
    assert resp_json.get("msg") == "Ledger operation succesfully completed!"
