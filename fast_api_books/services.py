from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Receipt
from schemas import ReceiptSchemaIn


async def get_all_receipts_from_db(session: AsyncSession) -> list[Receipt]:
    result = await session.execute(select(Receipt).order_by(
        Receipt.views_counter.desc()
    ).order_by(
        Receipt.cooking_time.desc())
    )
    return result.scalars().all()


async def create_new_receipt_db(receipt: ReceiptSchemaIn, session: AsyncSession) -> Receipt:
    new_receipt = Receipt(**receipt.dict())
    session.add(new_receipt)
    await session.commit()
    return new_receipt
