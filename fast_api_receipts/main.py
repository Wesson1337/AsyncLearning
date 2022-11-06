from typing import List, Literal

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db
from dependencies import get_async_session
from schemas import ReceiptSchemaOut, ReceiptSchemaIn, ReceiptSchemaPatch
from services import get_all_receipts_db, create_new_receipt_db, get_certain_receipt_db, patch_receipt_db, \
    delete_receipt_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get('/receipts', response_model=List[ReceiptSchemaOut])
async def get_all_receipts(
        session: AsyncSession = Depends(get_async_session)
) -> list[ReceiptSchemaOut]:

    receipts = await get_all_receipts_db(session)
    return receipts


@app.post('/receipts', response_model=ReceiptSchemaOut)
async def create_receipt(
        receipt: ReceiptSchemaIn,
        session: AsyncSession = Depends(get_async_session)
) -> ReceiptSchemaOut:

    new_receipt = await create_new_receipt_db(receipt, session)
    return new_receipt


@app.get('/receipts/{pk}', response_model=ReceiptSchemaOut)
async def get_certain_receipt(
        pk: int,
        session: AsyncSession = Depends(get_async_session)
) -> ReceiptSchemaOut:

    receipt = await get_certain_receipt_db(pk, session)
    return receipt


@app.patch('/receipts/{pk}', response_model=ReceiptSchemaOut)
async def patch_receipt(
        pk: int,
        receipt: ReceiptSchemaPatch,
        session: AsyncSession = Depends(get_async_session)
) -> ReceiptSchemaOut:

    updated_receipt = await patch_receipt_db(pk, receipt, session)
    return updated_receipt


@app.delete('/receipts/{pk}')
async def delete_receipt(
        pk: int,
        session: AsyncSession = Depends(get_async_session)
) -> dict[Literal["message"], str]:

    response = await delete_receipt_db(pk, session)
    return response
