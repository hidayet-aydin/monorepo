### Running the Application

To run the application, use the following command in your terminal:

```bash
uvicorn --reload main:app
```

### Testing the LedgerAPI

You can test the ledger API using pytest.

```bash
pytest api/routers/test_ledger.py
```

**Results:**

```
platform darwin -- Python 3.10.16, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/hidayet/Downloads/shared_ledger_ystem/app
plugins: anyio-4.8.0
collected 6 items

api/routers/test_ledger.py ......
```
