"""Seed runner - populates initial data for the platform."""

from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import async_session_factory
from app.infrastructure.database.models.obligation import ObligationType, ObligationPeriodicity
from app.infrastructure.database.models.fiscal_year import FiscalYear
from app.infrastructure.database.models.threshold import Threshold
from app.infrastructure.database.models.rule import RuleSet, Rule, RuleCondition
from app.infrastructure.database.models.disclaimer import DisclaimerVersion

from app.seeds.obligation_types import OBLIGATION_TYPES
from app.seeds.fiscal_year_2025 import FISCAL_YEAR_2025, PERIODICITIES_2025
from app.seeds.thresholds_2025 import THRESHOLDS_2025
from app.seeds.rules_2025 import RULES_2025


async def seed_obligation_types(db: AsyncSession) -> dict[str, uuid.UUID]:
    """Seed obligation types and return code -> id mapping."""
    mapping: dict[str, uuid.UUID] = {}

    for ot_data in OBLIGATION_TYPES:
        result = await db.execute(
            select(ObligationType).where(ObligationType.code == ot_data["code"])
        )
        existing = result.scalar_one_or_none()
        if existing:
            mapping[ot_data["code"]] = existing.id
            continue

        ot = ObligationType(id=uuid.uuid4(), **ot_data)
        db.add(ot)
        mapping[ot_data["code"]] = ot.id

    await db.flush()
    print(f"  Seeded {len(mapping)} obligation types")
    return mapping


async def seed_fiscal_year(db: AsyncSession) -> uuid.UUID:
    """Seed fiscal year 2025 and return its ID."""
    result = await db.execute(
        select(FiscalYear).where(FiscalYear.year == FISCAL_YEAR_2025["year"])
    )
    existing = result.scalar_one_or_none()
    if existing:
        print(f"  Fiscal year {FISCAL_YEAR_2025['year']} already exists")
        return existing.id

    fy = FiscalYear(id=uuid.uuid4(), **FISCAL_YEAR_2025)
    db.add(fy)
    await db.flush()
    print(f"  Seeded fiscal year {FISCAL_YEAR_2025['year']}")
    return fy.id


async def seed_thresholds(db: AsyncSession, fiscal_year_id: uuid.UUID) -> None:
    """Seed thresholds for 2025."""
    for t_data in THRESHOLDS_2025:
        result = await db.execute(
            select(Threshold).where(
                Threshold.fiscal_year_id == fiscal_year_id,
                Threshold.code == t_data["code"],
            )
        )
        if result.scalar_one_or_none():
            continue
        t = Threshold(id=uuid.uuid4(), fiscal_year_id=fiscal_year_id, **t_data)
        db.add(t)

    await db.flush()
    print(f"  Seeded {len(THRESHOLDS_2025)} thresholds")


async def seed_periodicities(
    db: AsyncSession,
    fiscal_year_id: uuid.UUID,
    obligation_mapping: dict[str, uuid.UUID],
) -> None:
    """Seed obligation periodicities for 2025."""
    for p_data in PERIODICITIES_2025:
        ob_id = obligation_mapping.get(p_data["obligation_code"])
        if not ob_id:
            continue

        result = await db.execute(
            select(ObligationPeriodicity).where(
                ObligationPeriodicity.obligation_type_id == ob_id,
                ObligationPeriodicity.fiscal_year_id == fiscal_year_id,
            )
        )
        if result.scalar_one_or_none():
            continue

        op = ObligationPeriodicity(
            id=uuid.uuid4(),
            obligation_type_id=ob_id,
            fiscal_year_id=fiscal_year_id,
            frequency=p_data["frequency"],
            description=p_data["description"],
        )
        db.add(op)

    await db.flush()
    print(f"  Seeded periodicities")


async def seed_rules(
    db: AsyncSession,
    fiscal_year_id: uuid.UUID,
    obligation_mapping: dict[str, uuid.UUID],
) -> None:
    """Seed rule set and rules for 2025."""
    result = await db.execute(
        select(RuleSet).where(
            RuleSet.fiscal_year_id == fiscal_year_id,
            RuleSet.version == 1,
        )
    )
    existing_rs = result.scalar_one_or_none()
    if existing_rs:
        print(f"  Rule set v1 already exists for fiscal year")
        return

    rs = RuleSet(
        id=uuid.uuid4(),
        fiscal_year_id=fiscal_year_id,
        version=1,
        status="active",
    )
    db.add(rs)
    await db.flush()

    for rule_data in RULES_2025:
        ob_id = obligation_mapping.get(rule_data["obligation_code"])
        if not ob_id:
            continue

        rule = Rule(
            id=uuid.uuid4(),
            rule_set_id=rs.id,
            obligation_type_id=ob_id,
            code=rule_data["code"],
            name=rule_data["name"],
            description=rule_data.get("description"),
            logic_operator=rule_data.get("logic_operator", "AND"),
            priority=rule_data.get("priority", 0),
            result_if_true=rule_data.get("result_if_true", "applies"),
            is_active=True,
        )
        db.add(rule)
        await db.flush()

        for cond_data in rule_data.get("conditions", []):
            cond = RuleCondition(
                id=uuid.uuid4(),
                rule_id=rule.id,
                field=cond_data["field"],
                operator=cond_data["operator"],
                value_type=cond_data["value_type"],
                value=cond_data.get("value"),
                value_secondary=cond_data.get("value_secondary"),
                description=cond_data.get("description"),
            )
            db.add(cond)

    await db.flush()
    print(f"  Seeded rule set v1 with {len(RULES_2025)} rules")


async def seed_disclaimer(db: AsyncSession) -> None:
    """Seed initial disclaimer."""
    result = await db.execute(
        select(DisclaimerVersion).where(DisclaimerVersion.version == 1)
    )
    if result.scalar_one_or_none():
        print("  Disclaimer v1 already exists")
        return

    disclaimer = DisclaimerVersion(
        id=uuid.uuid4(),
        version=1,
        content_es=(
            "Esta información es de carácter orientativo y educativo. No constituye asesoría "
            "tributaria, contable ni legal. No reemplaza la consulta con un contador público "
            "certificado. Los resultados se basan en las reglas vigentes y la información "
            "suministrada por el usuario. La plataforma no presenta declaraciones oficiales "
            "ni interactúa con entidades gubernamentales. Use esta información bajo su "
            "propia responsabilidad."
        ),
        content_en=(
            "This information is for guidance and educational purposes only. It does not "
            "constitute tax, accounting, or legal advice. It does not replace consultation "
            "with a certified public accountant. Results are based on current rules and "
            "user-provided information. The platform does not file official declarations "
            "or interact with government entities. Use this information at your own risk."
        ),
        is_current=True,
    )
    db.add(disclaimer)
    await db.flush()
    print("  Seeded disclaimer v1")


async def run_all_seeds() -> None:
    print("Running seeds...")
    async with async_session_factory() as db:
        obligation_mapping = await seed_obligation_types(db)
        fiscal_year_id = await seed_fiscal_year(db)
        await seed_thresholds(db, fiscal_year_id)
        await seed_periodicities(db, fiscal_year_id, obligation_mapping)
        await seed_rules(db, fiscal_year_id, obligation_mapping)
        await seed_disclaimer(db)
        await db.commit()
    print("Seeds completed!")


if __name__ == "__main__":
    asyncio.run(run_all_seeds())
