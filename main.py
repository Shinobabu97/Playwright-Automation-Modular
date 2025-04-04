import asyncio
import os
from playwright.async_api import async_playwright
from ups_downloader import download_blob_pdf_from_tab

SAVE_DIR = r"C:\Users\wn00246424\OneDrive - WGS 365\SHINO"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        # Find the invoice page
        page = next((p for p in context.pages if "billing.ups.com/ups/billing/invoice" in p.url), None)
        if not page:
            print("Invoice page not found.")
            return

        # Locate the invoice PDF button and click it
        pdf_click_xpath = '//*[@id="invoice-table_wrapper"]/div[2]/div/table/tbody/tr[1]/td[10]/div'
        async with context.expect_page() as new_tab_info:
            await page.locator(f"xpath={pdf_click_xpath}").click()

        blob_tab = await new_tab_info.value
        invoice_number = "example_invoice"
        save_path = os.path.join(SAVE_DIR, f"{invoice_number}.pdf") #fetching the invoice number

        # Download and close
        await download_blob_pdf_from_tab(blob_tab, save_path)
        await blob_tab.close()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(run())
