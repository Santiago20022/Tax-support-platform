"""Integration tests for auth endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, sample_tenant):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepass123",
            "full_name": "New User",
            "tenant_slug": sample_tenant.slug,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, sample_user, sample_tenant):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": sample_user.email,
            "password": "securepass123",
            "full_name": "Duplicate User",
            "tenant_slug": sample_tenant.slug,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, sample_user, sample_tenant):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": sample_user.email,
            "password": "testpass123",
            "tenant_slug": sample_tenant.slug,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == sample_user.email


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, sample_user, sample_tenant):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": sample_user.email,
            "password": "wrongpassword",
            "tenant_slug": sample_tenant.slug,
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, sample_user, sample_tenant):
    # First login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": sample_user.email,
            "password": "testpass123",
            "tenant_slug": sample_tenant.slug,
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    # Then refresh
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
