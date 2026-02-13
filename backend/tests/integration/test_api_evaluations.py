"""Integration tests for evaluation endpoints."""

import uuid
from decimal import Decimal

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.fiscal_year import FiscalYear
from app.infrastructure.database.models.obligation import ObligationType, ObligationPeriodicity
from app.infrastructure.database.models.rule import Rule, RuleCondition, RuleSet
from app.infrastructure.database.models.threshold import Threshold


@pytest_asyncio.fixture
async def seeded_data(db_session: AsyncSession):
    """Seed a complete rule set for testing evaluation."""
    # Fiscal Year
    fy = FiscalYear(
        id=uuid.uuid4(),
        year=2099,
        status="active",
        uvt_value=Decimal("49641"),
    )
    db_session.add(fy)
    await db_session.flush()

    # Obligation Type
    renta = ObligationType(
        id=uuid.uuid4(),
        code="renta_test",
        name="Renta Test",
        category="nacional",
        description="Renta test obligation",
        responsible_entity="DIAN",
        legal_base="Art. 592 ET",
    )
    db_session.add(renta)
    await db_session.flush()

    # Threshold
    threshold = Threshold(
        id=uuid.uuid4(),
        fiscal_year_id=fy.id,
        code="renta_test_tope",
        label="Tope renta test",
        value_uvt=Decimal("1400"),
        value_cop=Decimal("69497400"),
    )
    db_session.add(threshold)

    # Periodicity
    periodicity = ObligationPeriodicity(
        id=uuid.uuid4(),
        obligation_type_id=renta.id,
        fiscal_year_id=fy.id,
        frequency="anual",
    )
    db_session.add(periodicity)

    # Rule Set
    rs = RuleSet(
        id=uuid.uuid4(),
        fiscal_year_id=fy.id,
        version=1,
        status="active",
    )
    db_session.add(rs)
    await db_session.flush()

    # Rule
    rule = Rule(
        id=uuid.uuid4(),
        rule_set_id=rs.id,
        obligation_type_id=renta.id,
        code="renta_test_rule",
        name="Renta test rule",
        logic_operator="OR",
        priority=1,
        result_if_true="applies",
    )
    db_session.add(rule)
    await db_session.flush()

    # Rule Condition
    cond = RuleCondition(
        id=uuid.uuid4(),
        rule_id=rule.id,
        field="ingresos_brutos_cop",
        operator="gte",
        value_type="threshold_ref",
        value="renta_test_tope",
        description="Ingresos >= 1400 UVT",
    )
    db_session.add(cond)
    await db_session.flush()

    return {"fiscal_year": fy, "obligation": renta}


@pytest.mark.asyncio
async def test_create_evaluation(
    client: AsyncClient, auth_headers, seeded_data, db_session: AsyncSession
):
    fy = seeded_data["fiscal_year"]

    # Create profile first
    profile_response = await client.post(
        "/api/v1/profiles",
        json={
            "fiscal_year_id": str(fy.id),
            "persona_type": "natural_comerciante",
            "regime": "ordinario",
            "is_iva_responsable": False,
            "ingresos_brutos_cop": 180000000,
            "patrimonio_bruto_cop": 200000000,
            "has_employees": False,
        },
        headers=auth_headers,
    )
    assert profile_response.status_code == 201
    profile_id = profile_response.json()["id"]

    # Create evaluation
    eval_response = await client.post(
        "/api/v1/evaluations",
        json={"tax_profile_id": profile_id},
        headers=auth_headers,
    )
    assert eval_response.status_code == 201
    data = eval_response.json()

    assert "id" in data
    assert "results" in data
    assert "summary" in data
    assert "disclaimer" in data
    assert data["disclaimer"]["is_informational_only"] is True

    # Check that results contain our obligation
    results = data["results"]
    assert len(results) >= 1
    renta_result = next(
        (r for r in results if r["obligation"]["code"] == "renta_test"), None
    )
    assert renta_result is not None
    assert renta_result["result"] == "applies"


@pytest.mark.asyncio
async def test_list_evaluations(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/evaluations", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_evaluation_not_found(client: AsyncClient, auth_headers):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/evaluations/{fake_id}", headers=auth_headers)
    assert response.status_code == 404
