from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ParcelType


async def get_parcel_type_by_id(
    parcel_type_id: int, db: AsyncSession
) -> ParcelType | None:
    query = select(ParcelType).where(ParcelType.id == parcel_type_id)
    result = await db.execute(query)
    return result.scalars().one_or_none()


async def get_all_parcel_types(db: AsyncSession) -> Sequence[ParcelType]:
    query = select(ParcelType)
    result = await db.execute(query)
    return result.scalars().all()
