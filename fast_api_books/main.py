from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db
from dependencies import get_async_session
from schemas import ReceiptSchemaOut, ReceiptSchemaIn
from services import get_all_receipts_from_db, create_new_receipt_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get('/receipts', response_model=List[ReceiptSchemaOut])
async def get_all_receipts(
        session: AsyncSession = Depends(get_async_session)
) -> list[ReceiptSchemaOut]:

    receipts = await get_all_receipts_from_db(session)
    return receipts


@app.post('/receipts', response_model=ReceiptSchemaOut)
async def create_receipt(
        receipt: ReceiptSchemaIn,
        session: AsyncSession = Depends(get_async_session)
) -> ReceiptSchemaOut:

    new_receipt = await create_new_receipt_db(receipt, session)
    return new_receipt
