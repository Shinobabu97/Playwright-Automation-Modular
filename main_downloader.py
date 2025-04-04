import asyncio
import os
from playwright.async_api import async_playwright
from downloader.blob_utils import download_blob_pdf_from_tab
from downloader.click_download import download_file  # <- Import the alt-click PDF downloader

SAVE_DIR = r"C:\\Users\\wn00246424\\OneDrive - WGS 365\\SHINO"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        # Try to find the page with the UPS invoices
        page = next((p for p in context.pages if "billing.ups.com/ups/billing/invoice" in p.url), None) #Give the default page mention in GUI Launcher
        if not page:
            print("Invoice page not found.")
            return

        # === Example 1: Download a blob PDF (opens in new tab) ===
        pdf_click_xpath = '//*[@id="invoice-table_wrapper"]/div[2]/div/table/tbody/tr[1]/td[10]/div'
        async with context.expect_page() as new_tab_info:
            await page.locator(f"xpath={pdf_click_xpath}").click()
        blob_tab = await new_tab_info.value

        invoice_number = "example_invoice"
        save_path = os.path.join(SAVE_DIR, f"{invoice_number}.pdf")
        await download_blob_pdf_from_tab(blob_tab, save_path)
        await blob_tab.close()
        print("Blob PDF download complete.\n")

        # === Example 2: Alt-click a link to trigger download directly ===
        alt_click_xpath = '//*[@id="download-link-alt"]'  # Replace with actual XPath of the download link
        await download_file(
            page=page,
            download_xpath=alt_click_xpath,
            download_folder=SAVE_DIR,
            custom_filename="alt_click_invoice"
        )
        print("Alt-click PDF download complete.")

if __name__ == "__main__":
    asyncio.run(run())
