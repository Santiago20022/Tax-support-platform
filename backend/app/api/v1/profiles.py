from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_current_user
from app.api.v1.schemas.profiles import (
    ProfileCreateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.application.profile_service import ProfileService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.pg_profile_repo import PgProfileRepository

router = APIRouter(prefix="/profiles", tags=["profiles"])


def _to_response(entity) -> ProfileResponse:
    return ProfileResponse(
        id=str(entity.id),
        user_id=str(entity.user_id),
        fiscal_year_id=str(entity.fiscal_year_id),
        persona_type=entity.persona_type,
        regime=entity.regime,
        is_iva_responsable=entity.is_iva_responsable,
        ingresos_brutos_cop=float(entity.ingresos_brutos_cop),
        economic_activity_ciiu=entity.economic_activity_ciiu,
        patrimonio_bruto_cop=float(entity.patrimonio_bruto_cop) if entity.patrimonio_bruto_cop else None,
        has_employees=entity.has_employees,
        employee_count=entity.employee_count,
        city=entity.city,
        department=entity.department,
        has_rut=entity.has_rut,
        has_comercio_registration=entity.has_comercio_registration,
        nit_last_digit=entity.nit_last_digit,
        consignaciones_cop=float(entity.consignaciones_cop) if entity.consignaciones_cop else None,
        compras_consumos_cop=float(entity.compras_consumos_cop) if entity.compras_consumos_cop else None,
    )


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    request: ProfileCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = ProfileService(PgProfileRepository(db))
    profile = await service.create_profile(
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        fiscal_year_id=UUID(request.fiscal_year_id),
        data=request.model_dump(),
    )
    return _to_response(profile)


@router.get("", response_model=list[ProfileResponse])
async def list_profiles(
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = ProfileService(PgProfileRepository(db))
    profiles = await service.list_profiles(user.user_id, user.tenant_id)
    return [_to_response(p) for p in profiles]


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = ProfileService(PgProfileRepository(db))
    profile = await service.get_profile(UUID(profile_id), user.tenant_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return _to_response(profile)


@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: str,
    request: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = ProfileService(PgProfileRepository(db))
    try:
        profile = await service.update_profile(
            UUID(profile_id), user.tenant_id, request.model_dump(exclude_none=True)
        )
        return _to_response(profile)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = ProfileService(PgProfileRepository(db))
    deleted = await service.delete_profile(UUID(profile_id), user.tenant_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
