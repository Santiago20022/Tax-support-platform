import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

/** Helper: create a profile via wizard (auto-shown for new user) and get redirected to evaluation detail. */
async function createProfileAndEvaluate(page: import("@playwright/test").Page) {
  await registerAndLogin(page);

  // Wizard auto-shows for new users
  await page.goto("/perfil");
  await expect(
    page.getByRole("heading", { name: "Nuevo Perfil Tributario" }),
  ).toBeVisible({ timeout: 10000 });

  // Step 0
  await page.locator("#fiscal_year_id").selectOption({ index: 1 });
  await page.locator("#persona_type").selectOption("natural");
  await page.locator("#regime").selectOption("ordinario");
  await page.locator("#is_iva_responsable").check();
  await page.getByRole("button", { name: "Siguiente" }).click();

  // Step 1
  await page.locator("#ingresos_brutos_cop").fill("150000000");
  await page.locator("#patrimonio_bruto_cop").fill("500000000");
  await page.locator("#consignaciones_cop").fill("200000000");
  await page.locator("#compras_consumos_cop").fill("50000000");
  await page.getByRole("button", { name: "Siguiente" }).click();

  // Step 2
  await page.locator("#economic_activity_ciiu").fill("4711");
  await page.locator("#has_rut").check();
  await page.locator("#has_comercio_registration").check();
  await page.getByRole("button", { name: "Siguiente" }).click();

  // Step 3
  await page.locator("#city").fill("Bogotá");
  await page.locator("#department").fill("Cundinamarca");
  await page.locator("#has_employees").check();
  await page.locator("#employee_count").fill("5");
  await page.getByRole("button", { name: "Siguiente" }).click();

  // Step 4
  await page.locator("#nit_last_digit").fill("7");
  await page.getByRole("button", { name: "Crear Perfil y Evaluar" }).click();

  await expect(page).toHaveURL(/\/evaluacion\//, { timeout: 15000 });
}

test.describe("Evaluation", () => {
  test("evaluation detail page shows results grouped by category", async ({ page }) => {
    await createProfileAndEvaluate(page);

    await expect(page.getByRole("heading", { name: "Resultados" })).toBeVisible();

    // Should have result badges (Aplica / No aplica / etc)
    const resultBadges = page.getByText(/Aplica|No aplica|Condicional|Requiere más info/);
    await expect(resultBadges.first()).toBeVisible({ timeout: 5000 });
  });

  test("result summary shows applies/does_not_apply counts", async ({ page }) => {
    await createProfileAndEvaluate(page);

    // The summary section displays stat cards with labels
    await expect(page.getByText("Aplican").first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText("No aplican").first()).toBeVisible();
  });
});
