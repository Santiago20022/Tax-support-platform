from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_current_user
from app.api.v1.schemas.evaluations import (
    DisclaimerResponse,
    EvaluationCreateRequest,
    EvaluationListItemResponse,
    EvaluationResponse,
    EvaluationResultResponse,
    EvaluationSummaryResponse,
    ObligationResponse,
)
from app.application.evaluation_service import EvaluationService
from app.domain.entities.evaluation import EvaluationEntity
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.pg_evaluation_repo import PgEvaluationRepository
from app.infrastructure.repositories.pg_profile_repo import PgProfileRepository
from app.infrastructure.repositories.pg_rule_repo import PgRuleRepository
from app.infrastructure.repositories.pg_threshold_repo import PgThresholdRepository

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

DISCLAIMER_TEXT = (
    "Esta información es de carácter orientativo y educativo. No constituye asesoría "
    "tributaria, contable ni legal. No reemplaza la consulta con un contador público "
    "certificado. Los resultados se basan en las reglas vigentes y la información "
    "suministrada por el usuario."
)


def _build_service(db: AsyncSession) -> EvaluationService:
    return EvaluationService(
        db=db,
        profile_repo=PgProfileRepository(db),
        rule_repo=PgRuleRepository(db),
        evaluation_repo=PgEvaluationRepository(db),
        threshold_repo=PgThresholdRepository(db),
    )


def _to_response(evaluation: EvaluationEntity) -> EvaluationResponse:
    results = []
    for r in evaluation.results:
        results.append(
            EvaluationResultResponse(
                obligation=ObligationResponse(
                    code=r.obligation_code,
                    name=r.obligation_name,
                    responsible_entity=r.responsible_entity,
                ),
                result=r.result,
                periodicity=r.periodicity,
                explanation=r.explanation_es,
                legal_references=r.legal_references,
                conditions_evaluated=r.conditions_evaluated,
            )
        )

    summary = evaluation.summary()

    return EvaluationResponse(
        id=str(evaluation.id),
        evaluated_at=evaluation.evaluated_at.isoformat(),
        profile_summary=evaluation.profile_snapshot,
        results=results,
        summary=EvaluationSummaryResponse(**summary),
        disclaimer=DisclaimerResponse(
            version=1,
            text=DISCLAIMER_TEXT,
            is_informational_only=True,
        ),
    )


@router.post("", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    request: EvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = _build_service(db)
    try:
        evaluation = await service.evaluate(
            tax_profile_id=UUID(request.tax_profile_id),
            user_id=user.user_id,
            tenant_id=user.tenant_id,
        )
        return _to_response(evaluation)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[EvaluationListItemResponse])
async def list_evaluations(
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = _build_service(db)
    evaluations = await service.list_evaluations(user.user_id, user.tenant_id)
    return [
        EvaluationListItemResponse(
            id=str(e.id),
            fiscal_year_id=str(e.fiscal_year_id),
            status=e.status,
            evaluated_at=e.evaluated_at.isoformat(),
            summary=EvaluationSummaryResponse(**e.summary()),
        )
        for e in evaluations
    ]


@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = _build_service(db)
    evaluation = await service.get_evaluation(UUID(evaluation_id), user.tenant_id)
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found")
    return _to_response(evaluation)
