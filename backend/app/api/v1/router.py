from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.evaluations import router as evaluations_router
from app.api.v1.obligations import router as obligations_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.disclaimers import router as disclaimers_router
from app.api.v1.fiscal_years_public import router as fiscal_years_public_router
from app.api.v1.admin.fiscal_years import router as admin_fiscal_years_router
from app.api.v1.admin.rule_sets import router as admin_rule_sets_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(profiles_router)
api_v1_router.include_router(evaluations_router)
api_v1_router.include_router(obligations_router)
api_v1_router.include_router(calendar_router)
api_v1_router.include_router(disclaimers_router)
api_v1_router.include_router(fiscal_years_public_router)
api_v1_router.include_router(admin_fiscal_years_router)
api_v1_router.include_router(admin_rule_sets_router)
