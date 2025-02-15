from fastapi import FastAPI, Depends

from api.routers import ledgers
from dependencies import get_token_header

app = FastAPI()

app.include_router(ledgers.router, dependencies=[Depends(get_token_header)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
