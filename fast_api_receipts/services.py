from datetime import datetime
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Receipt
from schemas import ReceiptSchemaIn, ReceiptSchemaPatch


async def get_all_receipts_db(session: AsyncSession) -> list[Receipt]:
    result = await session.execute(select(Receipt).order_by(
        Receipt.views_counter.desc()
    ).order_by(
        Receipt.cooking_time)
    )
    return result.scalars().all()


async def create_new_receipt_db(receipt: ReceiptSchemaIn, session: AsyncSession) -> Receipt:
    new_receipt = Receipt(**receipt.dict())
    session.add(new_receipt)
    await session.commit()
    return new_receipt


async def get_certain_receipt_db(pk: int, session: AsyncSession) -> Receipt:
    receipt = await session.get(Receipt, {'id': pk})
    await increment_views_counter(receipt, session)
    return receipt


async def increment_views_counter(receipt: Receipt, session: AsyncSession) -> None:
    receipt.views_counter += 1
    await session.commit()


async def patch_receipt_db(pk: int, receipt: ReceiptSchemaPatch, session: AsyncSession) -> Receipt:
    receipt_data = receipt.dict(exclude_unset=True)
    stored_receipt = await session.get(Receipt, {'id': pk})

    for k, v in receipt_data.items():
        if k and v:
            setattr(stored_receipt, k, v)
    stored_receipt.updated = datetime.now()

    await session.commit()
    updated_receipt = stored_receipt
    return updated_receipt


async def delete_receipt_db(pk: int, session: AsyncSession) -> dict[Literal["message"], str]:
    receipt = await session.get(Receipt, {'id': pk})
    if receipt:
        await session.delete(receipt)
        await session.commit()
        return {"message": "done"}
    else:
        return {"message": "receipt doesn't exists"}
