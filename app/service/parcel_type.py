from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ParcelType
from app.repository import parcel_type as parcel_type_repository


async def get_parcel_type(parcel_type_id: int, db: AsyncSession) -> ParcelType:
    parcel_type = await parcel_type_repository.get_parcel_type_by_id(parcel_type_id, db)
    if not parcel_type:
        raise HTTPException(status_code=404, detail="Тип посылки с таким id не найден")
    return parcel_type


async def get_all_parcel_types(db: AsyncSession) -> Sequence[ParcelType]:
    result = await parcel_type_repository.get_all_parcel_types(db)
    return result
