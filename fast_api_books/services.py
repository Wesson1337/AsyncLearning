from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api_books.models import Receipt


async def get_all_receipts_from_db(session: AsyncSession) -> list[Receipt]:
    result = await session.execute(select(Receipt).order_by(
        Receipt.views_counter.desc()
    ).order_by(
        Receipt.cooking_time.desc())
    )
    return result.scalars().all()

async def create_new_receipt(session: AsyncSession) -> Receipt: