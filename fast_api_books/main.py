from typing import List

from fastapi import FastAPI, Depends

from fast_api_books.dependencies import get_async_session
from fast_api_books.schemas import ReceiptSchemaOut, ReceiptSchemaIn
from fast_api_books.services import get_all_receipts_from_db

app = FastAPI()


@app.get('/receipts', response_model=List[ReceiptSchemaOut])
async def get_all_receipts(session: Depends(get_async_session)) -> list[ReceiptSchemaOut]:
    receipts = await get_all_receipts_from_db(session)
    return receipts


@app.post('/receipts', response_model=List[ReceiptSchemaOut])
async def create_receipt(receipt: ReceiptSchemaIn, session: Depends(get_async_session)) -> ReceiptSchemaOut:
    rece