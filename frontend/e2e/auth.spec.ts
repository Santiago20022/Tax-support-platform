import { test, expect } from "@playwright/test";
import { registerAndLogin, loginWith, uniqueEmail } from "./helpers";

test.describe("Authentication", () => {
  test("login page renders with correct heading and fields", async ({ page }) => {
    await page.goto("/login");

    await expect(page.getByRole("heading", { name: "Bienvenido de nuevo" })).toBeVisible();
    await expect(page.locator("#email")).toBeVisible();
    await expect(page.locator("#password")).toBeVisible();
    await expect(page.getByRole("button", { name: "Iniciar sesión" })).toBeVisible();
  });

  test("register new user redirects to /dashboard", async ({ page }) => {
    await registerAndLogin(page);

    await expect(page).toHaveURL(/\/dashboard/);
    await expect(page.getByRole("heading", { name: /Hola/ })).toBeVisible();
  });

  test("login with registered user redirects to /dashboard", async ({ page }) => {
    // First register a user
    const { email } = await registerAndLogin(page);

    // Logout by clearing storage and navigating to login
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    await page.goto("/login");

    // Login with the same credentials
    await loginWith(page, email);
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });
    await expect(page.getByRole("heading", { name: /Hola/ })).toBeVisible();
  });

  test("login with wrong credentials shows error alert", async ({ page }) => {
    await loginWith(page, "nonexistent@test.com", "WrongPassword123!");

    await expect(page.locator("[role='alert']")).toBeVisible({ timeout: 5000 });
  });

  test("protected route /dashboard redirects to /login when unauthenticated", async ({
    page,
  }) => {
    await page.goto("/dashboard");

    await expect(page).toHaveURL(/\/login/, { timeout: 10000 });
  });
});
