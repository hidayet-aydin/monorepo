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

Update Homebrew, install ncurses and pyenv:

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

### New Application Under "monorepo"

A new application has been added under the "monorepo" directory. This application utilizes the `LedgerOperation` class to perform operations.

```
| - app
|   | - db
|   |   | - init.py
|   |   | - models.py
|   |   | - schemas.py
```

New application schemas uses basically the `LedgerOperation` class to perform operations. It also includes a new schema for database operations.

`monorepo/app/db/schemas.py`

```python
from core.ledgers.schemas import BaseLedgerOperation, SHARED_OPERATION_VALUES

APP_OPERATION_VALUES = {
}

OPERATION_VALUES = {**APP_OPERATION_VALUES, **SHARED_OPERATION_VALUES}

LedgerOperation = BaseLedgerOperation("TypeOperations", OPERATION_VALUES)
```

### Database Installation

Using Docker to install PostgreSQL:

```bash
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -e POSTGRES_USER=admin -d postgres:16-bullseye
```

### Alembic Configuration

Alembic library is used to manage database migrations. It can be create a new database and apply future migrations.

Creating a new Alembic migration directory:

```bash
cd app
alembic init migrations
```

New directory structure for migrations:

```
| - app
|   | - db
|   | - migrations
|   |   | - versions
|   |   | - env.py
|   |   | - README
|   |   | - script.py.mako
|   | - alembic.ini
```

It must be configured with the correct database URL.

`app/alembic.ini`

```
sqlalchemy.url = postgresql://admin:12345@localhost:5432/postgres
```

Database models are defined in:

`app/migrations/env.py`

```python
from db.models import Base

target_metadata = Base.metadata
```

Next, it can be created an initial migration and apply it to the database:

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

Initial migration script is generated in versions directory. But, it is not applied to the database yet.

```
| - app
|   | - db
|   | - migrations
|   |   | - versions
|   |   |   | - af9a23125b82_initial_migration.py
|   |   | - env.py
|   |   | - README
|   |   | - script.py.mako
|   | - alembic.ini
```

To apply the migration to the database, run:

```bash
alembic upgrade head
```

If we want to add extra fields to the `LedgerOperation` class, we can modify the `monorepo/app/db/schemas.py` file.

```python
from core.ledgers.schemas import BaseLedgerOperation, SHARED_OPERATION_VALUES

APP_OPERATION_VALUES = {
    "CONTENT_CREATION": "CONTENT_CREATION",
    "CONTENT_ACCESS": "CONTENT_ACCESS"
}

OPERATION_VALUES = {**APP_OPERATION_VALUES, **SHARED_OPERATION_VALUES}

LedgerOperation = BaseLedgerOperation("TypeOperations", OPERATION_VALUES)
```

This will add the `CONTENT_CREATION` and `CONTENT_ACCESS` fields to the `LedgerOperation` class.

To apply the migration to the database, run:

```bash
alembic revision --autogenerate -m "adding new operations"
```

```
| - app
|   | - db
|   | - migrations
|   |   | - versions
|   |   |   | - af9a23125b82_initial_migration.py
|   |   |   | - 8cdc063783b2_adding_new_operations.py
|   |   | - env.py
|   |   | - README
|   |   | - script.py.mako
|   | - alembic.ini
```

But, creating a new migration file is not enought to add new fields to the database. We need to modify `8cdc063783b2_adding_new_operations.py` file.

```python
from db.schemas import OPERATION_VALUES

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
```

There are many ways to migrate the database schema for new Ledger operations. One way is to use SQLAlchemy's `op.execute()` method to run SQL commands directly on the database.

The migration will be applied to the database using Alembic.

```bash
alembic upgrade head
```

Finally, we can verify the changes.

**Initial Migration**

![Initial Migration](documents/pictures/initial_migration.png)

**After Migration For New Application**

![Initial Migration](documents/pictures/new_features.png)

### API Development

Database connection is established using SQLAlchemy's `create_engine()` method. The connection string includes the database name, user, password, and host. Database secrets are stored in a `.env` file and loaded using the `python-dotenv` library.

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=admin
DB_PASSWORD=12345
```

#### API Authentication

API authentication is handled using a token-based approach. The `x-token` header must be included in all API requests with the `secret-token`.

### Running the Application

```bash
uvicorn --reload main:app
```

#### Endpoints

Getting user credit info:

```bash
curl --location 'http://localhost:8000/ledger/user1' \
--header 'x-token: secret-token'
```

New user receiving credit:

```bash
curl --location 'http://localhost:8000/ledger' \
--header 'x-token: secret-token' \
--header 'Content-Type: application/json' \
--data '{
    "operation": "SIGNUP_CREDIT",
    "owner_id": "user1",
    "nonce": "2025-02-13T21:07:11.064Z"
} '
```

Spend credit:

```bash
curl --location 'http://localhost:8000/ledger' \
--header 'x-token: secret-token' \
--header 'Content-Type: application/json' \
--data '{
    "operation": "CREDIT_SPEND",
    "owner_id": "user1",
    "nonce": "2025-02-14T23:57:15.516Z"
} '
```
