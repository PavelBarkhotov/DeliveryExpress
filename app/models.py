from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    weight: Mapped[Decimal] = mapped_column(DECIMAL(6, 2))
    type_id: Mapped[int] = mapped_column(ForeignKey(ParcelType.id))
    parcel_type: Mapped["ParcelType"] = relationship()
    dollar_price: Mapped[Decimal] = mapped_column(DECIMAL(8, 2))
    delivery_price: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2), nullable=True
    )
    user_session: Mapped[str]

    __table_args__ = (Index("idx_session_type", "user_session", "type_id"),)
