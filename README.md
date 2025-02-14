# Shared Ledger System - POC Study

This repository contains a proof-of-concept (POC) study for a shared ledger system.

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
