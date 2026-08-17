from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.service import parcels as parcels_service
from app.dependency import get_session, get_user_session
from app.schemas import ParcelRequest, ParcelResponse, ParcelTypeResponse
from app.service import parcel_type as parcel_type_service

router = APIRouter()


@router.get("/parcels", response_model=list[ParcelResponse])
async def get_user_parcels(
    db: AsyncSession = Depends(get_session),
    user_session: str = Depends(get_user_session),
):
    return await parcels_service.get_user_parcels(db, user_session)


@router.get("/parcels/{parcel_id}", response_model=ParcelResponse)
async def get_user_parcel(
    parcel_id: int,
    db: AsyncSession = Depends(get_session),
    user_session: str = Depends(get_user_session),
):
    return await parcels_service.get_user_parcel(parcel_id, db, user_session)


@router.post(
    "/parcels", response_model=ParcelResponse, status_code=status.HTTP_201_CREATED
)
async def create_parcel(
    parcel: ParcelRequest,
    db: AsyncSession = Depends(get_session),
    user_session: str = Depends(get_user_session),
):
    return await parcels_service.create_parcel(parcel, db, user_session)


@router.get("/parcel-types", response_model=list[ParcelTypeResponse])
async def get_all_parcel_types(db: AsyncSession = Depends(get_session)):
    return await parcel_type_service.get_all_parcel_types(db)
