"""Evaluation service - orchestrates the full evaluation flow."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.engine.engine import RulesEngine
from app.domain.entities.evaluation import EvaluationEntity
from app.domain.entities.obligation import ObligationTypeEntity
from app.domain.entities.rule import RuleEntity
from app.domain.interfaces.evaluation_repository import EvaluationRepository
from app.domain.interfaces.profile_repository import ProfileRepository
from app.domain.interfaces.rule_repository import RuleRepository
from app.domain.interfaces.threshold_repository import ThresholdRepository
from app.infrastructure.database.models.fiscal_year import FiscalYear
from app.infrastructure.database.models.obligation import ObligationType, ObligationPeriodicity


class EvaluationService:
    def __init__(
        self,
        db: AsyncSession,
        profile_repo: ProfileRepository,
        rule_repo: RuleRepository,
        evaluation_repo: EvaluationRepository,
        threshold_repo: ThresholdRepository,
    ) -> None:
        self._db = db
        self._profile_repo = profile_repo
        self._rule_repo = rule_repo
        self._evaluation_repo = evaluation_repo
        self._threshold_repo = threshold_repo

    async def evaluate(
        self,
        tax_profile_id: UUID,
        user_id: UUID,
        tenant_id: UUID,
    ) -> EvaluationEntity:
        # 1. Load the profile
        profile = await self._profile_repo.get_by_id(tax_profile_id, tenant_id)
        if not profile:
            raise ValueError("Tax profile not found")
        if profile.user_id != user_id:
            raise ValueError("Profile does not belong to user")

        # 2. Load fiscal year
        fy_result = await self._db.execute(
            select(FiscalYear).where(FiscalYear.id == profile.fiscal_year_id)
        )
        fiscal_year = fy_result.scalar_one_or_none()
        if not fiscal_year:
            raise ValueError("Fiscal year not found")

        # 3. Load active rule set
        rule_set = await self._rule_repo.get_active_rule_set(fiscal_year.id)
        if not rule_set:
            raise ValueError(f"No active rule set for fiscal year {fiscal_year.year}")

        # 4. Load thresholds
        thresholds = await self._threshold_repo.get_thresholds_map(fiscal_year.id)

        # 5. Load obligation types
        obligations = await self._load_obligations()

        # 6. Build rules by obligation map
        rules_by_obligation: dict[UUID, list[RuleEntity]] = {}
        for rule in rule_set.rules:
            rules_by_obligation.setdefault(rule.obligation_type_id, []).append(rule)

        # 7. Run the engine
        engine = RulesEngine(thresholds=thresholds, fiscal_year=fiscal_year.year)
        results = engine.evaluate(profile, rule_set, obligations, rules_by_obligation)

        # 8. Enrich results with periodicity
        periodicities = await self._load_periodicities(fiscal_year.id)
        for result in results:
            key = result.obligation_type_id
            if key in periodicities:
                result.periodicity = periodicities[key]

        # 9. Create evaluation record
        evaluation = EvaluationEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            tenant_id=tenant_id,
            tax_profile_id=tax_profile_id,
            rule_set_id=rule_set.id,
            fiscal_year_id=fiscal_year.id,
            status="completed",
            evaluated_at=datetime.now(timezone.utc),
            profile_snapshot=profile.to_snapshot(),
            results=results,
        )

        await self._evaluation_repo.create(evaluation)
        return evaluation

    async def get_evaluation(
        self, evaluation_id: UUID, tenant_id: UUID
    ) -> EvaluationEntity | None:
        return await self._evaluation_repo.get_by_id(evaluation_id, tenant_id)

    async def list_evaluations(
        self, user_id: UUID, tenant_id: UUID
    ) -> list[EvaluationEntity]:
        return await self._evaluation_repo.list_by_user(user_id, tenant_id)

    async def _load_obligations(self) -> list[ObligationTypeEntity]:
        result = await self._db.execute(
            select(ObligationType)
            .where(ObligationType.is_active.is_(True))
            .order_by(ObligationType.display_order)
        )
        return [
            ObligationTypeEntity(
                id=o.id,
                code=o.code,
                name=o.name,
                category=o.category,
                description=o.description,
                responsible_entity=o.responsible_entity,
                legal_base=o.legal_base,
                is_active=o.is_active,
                display_order=o.display_order,
            )
            for o in result.scalars().all()
        ]

    async def _load_periodicities(self, fiscal_year_id: UUID) -> dict[UUID, str]:
        result = await self._db.execute(
            select(ObligationPeriodicity).where(
                ObligationPeriodicity.fiscal_year_id == fiscal_year_id
            )
        )
        return {
            p.obligation_type_id: p.frequency
            for p in result.scalars().all()
        }
