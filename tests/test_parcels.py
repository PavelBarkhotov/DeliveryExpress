from decimal import Decimal

import pytest


@pytest.mark.asyncio
async def test_parcel_create_happy_path(client):
    response = await client.post(
        "/api/v1/parcels",
        json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "string"
    assert Decimal(response.json()["weight"]) == 1
    assert Decimal(response.json()["dollar_price"]) == 1
