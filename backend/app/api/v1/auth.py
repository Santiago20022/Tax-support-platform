from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    TokenResponse,
)
from app.application.auth_service import AuthService
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        result = await service.register(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            tenant_slug=request.tenant_slug,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        result = await service.login(
            email=request.email,
            password=request.password,
            tenant_slug=request.tenant_slug,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        result = await service.refresh(request.refresh_token)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
