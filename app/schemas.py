from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class ParcelTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    name: str = Field(max_length=64)


class ParcelRequest(BaseModel):
    name: str = Field(max_length=64)
    weight: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    type_id: int = Field(gt=0)
    dollar_price: Decimal = Field(gt=0, max_digits=8, decimal_places=2)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Имя посылки не может быть пустым")
        return v


class ParcelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=64)
    weight: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    parcel_type: ParcelTypeResponse
    dollar_price: Decimal = Field(gt=0, max_digits=8, decimal_places=2)
    delivery_price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )

    @field_serializer("delivery_price")
    def return_str_if_none(self, v: None | Decimal) -> str | Decimal:
        if v is None:
            return "Не рассчитано"
        return v
