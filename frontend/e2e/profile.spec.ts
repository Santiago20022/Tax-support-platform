import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

test.describe("Tax Profile", () => {
  test("profile page shows wizard directly for new user with no profiles", async ({ page }) => {
    await registerAndLogin(page);

    await page.goto("/perfil");
    // When no profiles exist, the wizard is shown automatically
    await expect(
      page.getByRole("heading", { name: "Nuevo Perfil Tributario" }),
    ).toBeVisible({ timeout: 10000 });
  });

  test("complete 5-step wizard, auto-evaluates, redirects to evaluation detail", async ({
    page,
  }) => {
    await registerAndLogin(page);

    // Navigate to profile page — wizard auto-shows for new users
    await page.goto("/perfil");
    await expect(
      page.getByRole("heading", { name: "Nuevo Perfil Tributario" }),
    ).toBeVisible({ timeout: 10000 });

    // Step 0: Contributor type
    await page.locator("#fiscal_year_id").selectOption({ index: 1 });
    await page.locator("#persona_type").selectOption("natural");
    await page.locator("#regime").selectOption("ordinario");
    await page.locator("#is_iva_responsable").check();
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 1: Financial data
    await page.locator("#ingresos_brutos_cop").fill("150000000");
    await page.locator("#patrimonio_bruto_cop").fill("500000000");
    await page.locator("#consignaciones_cop").fill("200000000");
    await page.locator("#compras_consumos_cop").fill("50000000");
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 2: Economic activity
    await page.locator("#economic_activity_ciiu").fill("4711");
    await page.locator("#has_rut").check();
    await page.locator("#has_comercio_registration").check();
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 3: Location and employees
    await page.locator("#city").fill("Bogotá");
    await page.locator("#department").fill("Cundinamarca");
    await page.locator("#has_employees").check();
    await page.locator("#employee_count").fill("5");
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 4: Review + submit
    await page.locator("#nit_last_digit").fill("7");
    await page.getByRole("button", { name: "Crear Perfil y Evaluar" }).click();

    // Should redirect to evaluation detail
    await expect(page).toHaveURL(/\/evaluacion\//, { timeout: 15000 });
    await expect(page.getByRole("heading", { name: "Resultados" })).toBeVisible();
  });

  test("profile list shows created profile with correct data", async ({ page }) => {
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
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 1
    await page.locator("#ingresos_brutos_cop").fill("100000000");
    await page.locator("#patrimonio_bruto_cop").fill("200000000");
    await page.locator("#consignaciones_cop").fill("0");
    await page.locator("#compras_consumos_cop").fill("0");
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 2
    await page.locator("#economic_activity_ciiu").fill("6201");
    await page.locator("#has_rut").check();
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 3
    await page.locator("#city").fill("Medellín");
    await page.locator("#department").fill("Antioquia");
    await page.getByRole("button", { name: "Siguiente" }).click();

    // Step 4
    await page.locator("#nit_last_digit").fill("3");
    await page.getByRole("button", { name: "Crear Perfil y Evaluar" }).click();
    await expect(page).toHaveURL(/\/evaluacion\//, { timeout: 15000 });

    // Go to profile list
    await page.goto("/perfil");
    await expect(page.getByText("Persona Natural")).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("Régimen Ordinario")).toBeVisible();
  });
});
