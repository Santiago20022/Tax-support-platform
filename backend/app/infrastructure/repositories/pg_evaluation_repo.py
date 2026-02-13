from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.evaluation import EvaluationEntity, EvaluationResultEntity
from app.domain.interfaces.evaluation_repository import EvaluationRepository
from app.infrastructure.database.models.evaluation import Evaluation, EvaluationResult


class PgEvaluationRepository(EvaluationRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, evaluation: EvaluationEntity) -> EvaluationEntity:
        db_eval = Evaluation(
            id=evaluation.id or uuid.uuid4(),
            user_id=evaluation.user_id,
            tenant_id=evaluation.tenant_id,
            tax_profile_id=evaluation.tax_profile_id,
            rule_set_id=evaluation.rule_set_id,
            fiscal_year_id=evaluation.fiscal_year_id,
            status=evaluation.status,
            evaluated_at=evaluation.evaluated_at,
            profile_snapshot=evaluation.profile_snapshot,
        )
        self._db.add(db_eval)
        await self._db.flush()

        for result in evaluation.results:
            db_result = EvaluationResult(
                id=uuid.uuid4(),
                evaluation_id=db_eval.id,
                obligation_type_id=result.obligation_type_id,
                result=result.result,
                triggered_rule_id=result.triggered_rule_id,
                conditions_evaluated=result.conditions_evaluated,
                explanation_es=result.explanation_es,
                legal_references=result.legal_references,
                periodicity=result.periodicity,
                responsible_entity=result.responsible_entity,
            )
            self._db.add(db_result)

        await self._db.flush()
        return evaluation

    async def get_by_id(self, evaluation_id: UUID, tenant_id: UUID) -> EvaluationEntity | None:
        result = await self._db.execute(
            select(Evaluation)
            .options(selectinload(Evaluation.results))
            .where(
                Evaluation.id == evaluation_id,
                Evaluation.tenant_id == tenant_id,
            )
        )
        db_eval = result.scalar_one_or_none()
        return self._to_entity(db_eval) if db_eval else None

    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[EvaluationEntity]:
        result = await self._db.execute(
            select(Evaluation)
            .options(selectinload(Evaluation.results))
            .where(
                Evaluation.user_id == user_id,
                Evaluation.tenant_id == tenant_id,
            )
            .order_by(Evaluation.created_at.desc())
        )
        return [self._to_entity(e) for e in result.scalars().all()]

    @staticmethod
    def _to_entity(db: Evaluation) -> EvaluationEntity:
        return EvaluationEntity(
            id=db.id,
            user_id=db.user_id,
            tenant_id=db.tenant_id,
            tax_profile_id=db.tax_profile_id,
            rule_set_id=db.rule_set_id,
            fiscal_year_id=db.fiscal_year_id,
            status=db.status,
            evaluated_at=db.evaluated_at,
            profile_snapshot=db.profile_snapshot,
            results=[
                EvaluationResultEntity(
                    obligation_type_id=r.obligation_type_id,
                    obligation_code="",
                    obligation_name="",
                    result=r.result,
                    periodicity=r.periodicity,
                    responsible_entity=r.responsible_entity,
                    triggered_rule_id=r.triggered_rule_id,
                    conditions_evaluated=r.conditions_evaluated,
                    explanation_es=r.explanation_es,
                    legal_references=r.legal_references or [],
                )
                for r in db.results
            ]
            if db.results
            else [],
        )
