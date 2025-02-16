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
