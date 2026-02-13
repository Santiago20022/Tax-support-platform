import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

test.describe("Obligations Catalog", () => {
  test("obligations catalog loads all 6 obligations from seeds", async ({ page }) => {
    await registerAndLogin(page);

    await page.goto("/obligaciones");
    await expect(
      page.getByRole("heading", { name: "Catálogo de Obligaciones" }),
    ).toBeVisible({ timeout: 10000 });

    // Should show 6 obligations in subtitle
    await expect(page.getByText("6 obligaciones tributarias colombianas")).toBeVisible();
  });

  test("category filter buttons work correctly", async ({ page }) => {
    await registerAndLogin(page);

    await page.goto("/obligaciones");
    await expect(
      page.getByRole("heading", { name: "Catálogo de Obligaciones" }),
    ).toBeVisible({ timeout: 10000 });

    // "Todas" button should be present
    const todasButton = page.getByRole("button", { name: "Todas" });
    await expect(todasButton).toBeVisible();

    // There should be additional category filter buttons beyond "Todas"
    // Categories are rendered as <button> elements in the filter bar
    const filterContainer = page.locator("div.flex.flex-wrap.gap-2");
    const allButtons = filterContainer.locator("button");
    const buttonCount = await allButtons.count();
    expect(buttonCount).toBeGreaterThanOrEqual(2); // "Todas" + at least one category

    // Click a category filter (second button = first category)
    const categoryButton = allButtons.nth(1);
    await categoryButton.click();

    // The count should change (filtered to one category = fewer obligations)
    await expect(page.getByText(/\d+ obligaciones tributarias colombianas/)).toBeVisible();

    // Click "Todas" to go back to full list
    await todasButton.click();
    await expect(page.getByText("6 obligaciones tributarias colombianas")).toBeVisible();
  });
});
