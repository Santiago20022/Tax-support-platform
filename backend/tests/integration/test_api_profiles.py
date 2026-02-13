"""Integration tests for profile endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient, auth_headers, sample_fiscal_year):
    response = await client.post(
        "/api/v1/profiles",
        json={
            "fiscal_year_id": str(sample_fiscal_year.id),
            "persona_type": "natural_comerciante",
            "regime": "ordinario",
            "is_iva_responsable": False,
            "ingresos_brutos_cop": 180000000,
            "patrimonio_bruto_cop": 200000000,
            "has_employees": True,
            "employee_count": 3,
            "city": "Bogotá",
            "has_comercio_registration": True,
            "nit_last_digit": 7,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["persona_type"] == "natural_comerciante"
    assert data["ingresos_brutos_cop"] == 180000000
    assert data["has_employees"] is True


@pytest.mark.asyncio
async def test_list_profiles(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/profiles", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_and_get_profile(client: AsyncClient, auth_headers, sample_fiscal_year):
    # Create
    create_response = await client.post(
        "/api/v1/profiles",
        json={
            "fiscal_year_id": str(sample_fiscal_year.id),
            "persona_type": "natural",
            "regime": "simple",
            "is_iva_responsable": False,
            "ingresos_brutos_cop": 50000000,
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    # Get
    get_response = await client.get(f"/api/v1/profiles/{profile_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == profile_id


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, auth_headers, sample_fiscal_year):
    # Create
    create_response = await client.post(
        "/api/v1/profiles",
        json={
            "fiscal_year_id": str(sample_fiscal_year.id),
            "persona_type": "natural",
            "regime": "ordinario",
            "is_iva_responsable": False,
            "ingresos_brutos_cop": 50000000,
        },
        headers=auth_headers,
    )
    profile_id = create_response.json()["id"]

    # Update
    update_response = await client.put(
        f"/api/v1/profiles/{profile_id}",
        json={"ingresos_brutos_cop": 90000000},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["ingresos_brutos_cop"] == 90000000


@pytest.mark.asyncio
async def test_delete_profile(client: AsyncClient, auth_headers, sample_fiscal_year):
    # Create
    create_response = await client.post(
        "/api/v1/profiles",
        json={
            "fiscal_year_id": str(sample_fiscal_year.id),
            "persona_type": "natural",
            "regime": "ordinario",
            "is_iva_responsable": False,
            "ingresos_brutos_cop": 50000000,
        },
        headers=auth_headers,
    )
    profile_id = create_response.json()["id"]

    # Delete
    delete_response = await client.delete(f"/api/v1/profiles/{profile_id}", headers=auth_headers)
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/profiles")
    assert response.status_code == 403
