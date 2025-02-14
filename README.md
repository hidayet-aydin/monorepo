# Shared Ledger System - POC Study

This repository contains a proof-of-concept (POC) study for a shared ledger system. Type safety, code reuse, database design, and API design are emphasized in this study.

## Overview

This monorepo leverages a code reusability architecture, allowing core functions to be utilized across multiple applications. Each application is able to track user credits through a ledger system with its own specific operations.

## Requirements

- Python 3.10.16 or later
- PostgreSQL database (docker: postgres:16-bullseye)

## Installations

### Install Pyenv and Python on macOS

Installing Python with pyenv allows you to manage multiple Python versions easily.

Update Homebrew and install ncurses and pyenv:

```bash
brew update
brew install ncurses
brew install pyenv
pyenv install -l | less
pyenv install 3.10.16
pyenv versions
pyenv local 3.10.16
```

### Create a Virtual Environment and Install Dependencies

Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

requirements.txt file contains the following dependencies:

```
fastapi[standard]
python-dotenv==1.0.1
pydantic==2.10.6
SQLAlchemy==2.0.38
psycopg2-binary==2.9.10
alembic==1.14.1
python-dotenv==1.0.1
pytest==8.3.4
```

Install the dependencies using pip:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Postgres Installation

Using Docker to install PostgreSQL:

```bash
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -e POSTGRES_USER=admin -d postgres:16-bullseye
```

## Implementation Steps

### Core Functionality

All applications will use the same ledger logic from the monorepo core. BaseLedgerOperation and its subclasses have to be implemented as **Enums** class.

This is most common usage form that can be used in any application.

```python
class LedgerOperation(enum.Enum): # This should be more generic!
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
```

Instead of a direct class object, dependency injection is used to pass the operation object.

```python
from enum import Enum

class BaseLedgerOperation(str, Enum):
    def dummy(self):
        pass

SHARED_OPERATION_VALUES = {
    "DAILY_REWARD": "DAILY_REWARD",
    "SIGNUP_CREDIT": "SIGNUP_CREDIT",
    "CREDIT_SPEND": "CREDIT_SPEND",
    "CREDIT_ADD": "CREDIT_ADD"
}
```

Any application can now use the `LedgerOperation` class to perform operations without directly referencing the enum values. This enhances code reusability and maintainability.

```python
LedgerOperation = BaseLedgerOperation("TypeOperations", SHARED_OPERATION_VALUES)
```
