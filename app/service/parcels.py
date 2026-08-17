from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import parcels as parcels_repository
from app.service import parcel_type as parcel_type_service
from app.schemas import ParcelRequest


async def get_user_parcels(db: AsyncSession, user_session: str):
    result = await parcels_repository.get_all_parcels(db, user_session)
    if not result:
        raise HTTPException(status_code=404, detail="Посылки не были найдены")
    return result


async def get_user_parcel(parcel_id: int, db: AsyncSession, user_session: str):
    result = await parcels_repository.get_single_parcel(parcel_id, db, user_session)
    if not result:
        raise HTTPException(status_code=404, detail="Посылки с таким id не существует")
    return result


async def create_parcel(parcel: ParcelRequest, db: AsyncSession, user_session: str):
    parcel_type = await parcel_type_service.get_parcel_type(parcel.type_id, db)
    result = await parcels_repository.create_parcel(
        parcel, parcel_type, db, user_session
    )
    await db.commit()
    return result
