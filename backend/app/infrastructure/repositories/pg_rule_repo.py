from __future__ import annotations

import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.rule import RuleConditionEntity, RuleEntity, RuleSetEntity
from app.domain.interfaces.rule_repository import RuleRepository
from app.infrastructure.database.models.rule import Rule, RuleCondition, RuleSet


class PgRuleRepository(RuleRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_active_rule_set(self, fiscal_year_id: UUID) -> RuleSetEntity | None:
        result = await self._db.execute(
            select(RuleSet)
            .options(selectinload(RuleSet.rules).selectinload(Rule.conditions))
            .where(
                RuleSet.fiscal_year_id == fiscal_year_id,
                RuleSet.status == "active",
            )
        )
        db_rs = result.scalar_one_or_none()
        return self._to_entity(db_rs) if db_rs else None

    async def get_rules_for_obligation(
        self, rule_set_id: UUID, obligation_type_id: UUID
    ) -> list[RuleEntity]:
        result = await self._db.execute(
            select(Rule)
            .options(selectinload(Rule.conditions))
            .where(
                Rule.rule_set_id == rule_set_id,
                Rule.obligation_type_id == obligation_type_id,
                Rule.is_active.is_(True),
            )
            .order_by(Rule.priority)
        )
        return [self._rule_to_entity(r) for r in result.scalars().all()]

    async def get_rule_set_by_id(self, rule_set_id: UUID) -> RuleSetEntity | None:
        result = await self._db.execute(
            select(RuleSet)
            .options(selectinload(RuleSet.rules).selectinload(Rule.conditions))
            .where(RuleSet.id == rule_set_id)
        )
        db_rs = result.scalar_one_or_none()
        return self._to_entity(db_rs) if db_rs else None

    async def create_rule_set(self, rule_set: RuleSetEntity) -> RuleSetEntity:
        db_rs = RuleSet(
            id=rule_set.id or uuid.uuid4(),
            fiscal_year_id=rule_set.fiscal_year_id,
            version=rule_set.version,
            status=rule_set.status,
        )
        self._db.add(db_rs)
        await self._db.flush()
        return self._to_entity(db_rs)

    async def publish_rule_set(self, rule_set_id: UUID) -> RuleSetEntity:
        result = await self._db.execute(
            select(RuleSet).where(RuleSet.id == rule_set_id)
        )
        db_rs = result.scalar_one_or_none()
        if not db_rs:
            raise ValueError(f"RuleSet {rule_set_id} not found")

        # Deprecate current active rule set for this fiscal year
        active_result = await self._db.execute(
            select(RuleSet).where(
                RuleSet.fiscal_year_id == db_rs.fiscal_year_id,
                RuleSet.status == "active",
            )
        )
        for active_rs in active_result.scalars().all():
            active_rs.status = "deprecated"

        db_rs.status = "active"
        db_rs.published_at = datetime.now(timezone.utc)
        await self._db.flush()
        return self._to_entity(db_rs)

    def _to_entity(self, db: RuleSet) -> RuleSetEntity:
        return RuleSetEntity(
            id=db.id,
            fiscal_year_id=db.fiscal_year_id,
            version=db.version,
            status=db.status,
            rules=[self._rule_to_entity(r) for r in db.rules] if db.rules else [],
        )

    @staticmethod
    def _rule_to_entity(db: Rule) -> RuleEntity:
        return RuleEntity(
            id=db.id,
            rule_set_id=db.rule_set_id,
            obligation_type_id=db.obligation_type_id,
            code=db.code,
            name=db.name,
            description=db.description,
            logic_operator=db.logic_operator,
            priority=db.priority,
            result_if_true=db.result_if_true,
            is_active=db.is_active,
            conditions=[
                RuleConditionEntity(
                    id=c.id,
                    rule_id=c.rule_id,
                    field=c.field,
                    operator=c.operator,
                    value_type=c.value_type,
                    value=c.value,
                    value_secondary=c.value_secondary,
                    description=c.description,
                )
                for c in db.conditions
            ]
            if db.conditions
            else [],
        )
