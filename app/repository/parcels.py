from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Parcel, ParcelType
from app.schemas import ParcelRequest


async def get_all_parcels(
    limit: int,
    offset: int,
    type_id: int | None,
    calculated: bool | None,
    db: AsyncSession,
    user_session: str,
) -> Sequence[Parcel]:
    conditions = [Parcel.user_session == user_session]

    if type_id is not None:
        conditions.append(Parcel.type_id == type_id)

    if calculated is not None:
        conditions.append(
            Parcel.delivery_price.is_not(None)
            if calculated
            else Parcel.delivery_price.is_(None)
        )

    query = (
        select(Parcel)
        .where(*conditions)
        .options(selectinload(Parcel.parcel_type))
        .order_by(Parcel.id)
        .limit(limit)
        .offset(offset)
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


# Запрос для задачи Celery
async def get_all_parcels_for_task(
    limit: int,
    db: AsyncSession,
) -> Sequence[Parcel]:

    query = (
        select(Parcel)
        .where(Parcel.delivery_price.is_(None))
        .with_for_update(skip_locked=True)
        .order_by(Parcel.id)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()
