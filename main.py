from fastapi import FastAPI

from api import items, account
from core.database import database
from core.schemas import SuccessResponseSchema

app = FastAPI(title='back-end')

app.include_router(items.router)
app.include_router(account.router)


@app.get("/", response_model=SuccessResponseSchema, status_code=200)
async def root():
    return {
        "success": True,
        "message": "Api works fine."
    }


@app.on_event("startup")
async def connect_db():
    await database.connect()


@app.on_event("shutdown")
async def connect_db():
    await database.disconnect()


