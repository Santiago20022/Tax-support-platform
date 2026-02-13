import { type Page, expect } from "@playwright/test";

/** Generate a unique email to avoid conflicts between test runs. */
export function uniqueEmail(): string {
  return `e2e_${Date.now()}_${Math.random().toString(36).slice(2, 7)}@test.com`;
}

const TEST_PASSWORD = "TestPass123!";
const TEST_NAME = "E2E Test User";

/**
 * Register a fresh user via the UI and return the page already at /dashboard.
 * Each call creates a unique user so tests are independent.
 */
export async function registerAndLogin(page: Page): Promise<{ email: string }> {
  const email = uniqueEmail();

  await page.goto("/registro");
  await page.locator("#fullName").fill(TEST_NAME);
  await page.locator("#email").fill(email);
  await page.locator("#password").fill(TEST_PASSWORD);
  await page.locator("#confirmPassword").fill(TEST_PASSWORD);
  await page.getByRole("button", { name: "Crear cuenta" }).click();

  // Wait for redirect to dashboard
  await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });

  return { email };
}

/**
 * Login with existing credentials via the UI.
 */
export async function loginWith(
  page: Page,
  email: string,
  password: string = TEST_PASSWORD,
): Promise<void> {
  await page.goto("/login");
  await page.locator("#email").fill(email);
  await page.locator("#password").fill(password);
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
}
