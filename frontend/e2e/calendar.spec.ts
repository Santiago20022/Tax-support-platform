import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

test.describe("Calendar", () => {
  test("calendar page loads for authenticated user", async ({ page }) => {
    await registerAndLogin(page);

    await page.goto("/calendario");
    // New user with no evaluations sees empty state
    await expect(page.getByText("Calendario vacío")).toBeVisible({ timeout: 10000 });
  });
});
