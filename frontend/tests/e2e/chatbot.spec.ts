import { test, expect } from "@playwright/test";

test.describe("Flow RAG Chatbot", () => {
  test("allows user to send a message", async ({ page }) => {
    await page.goto("/");

    await page.getByLabel("Nickname").fill("Test User");
    await page.getByRole("button", { name: "Start chatting" }).click();

    await page.getByPlaceholder("Ask anything about Flow").fill("How do I authenticate?");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(page.getByText("How do I authenticate?")).toBeVisible();
  });
});
