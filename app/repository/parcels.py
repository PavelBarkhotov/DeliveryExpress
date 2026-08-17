from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Parcel
from app.schemas import ParcelRequest
from app.models import ParcelType


async def get_all_parcels(db: AsyncSession, user_session: str) -> Sequence[Parcel]:
    query = (
        select(Parcel)
        .where(Parcel.user_session == user_session)
        .options(selectinload(Parcel.parcel_type))
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_single_parcel(
    parcel_id: int, db: AsyncSession, user_session: str
) -> Parcel | None:
    query = (
        select(Parcel)
        .where(Parcel.id == parcel_id, Parcel.user_session == user_session)
        .options(selectinload(Parcel.parcel_type))
    )
    result = await db.execute(query)
    return result.scalars().one_or_none()


async def create_parcel(
    parcel: ParcelRequest, parcel_type: ParcelType, db: AsyncSession, user_session: str
) -> Parcel:
    item = Parcel(
        name=parcel.name,
        weight=parcel.weight,
        parcel_type=parcel_type,
        dollar_price=parcel.dollar_price,
        delivery_price=None,
        user_session=user_session,
    )
    db.add(item)
    await db.flush()
    return item
