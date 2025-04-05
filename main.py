import asyncio
import os
from playwright.async_api import async_playwright
from downloader.blob_download import download_blob_pdf_from_tab
from downloader.click_download import download_file

SAVE_DIR = os.getenv("UPS_OUTPUT_DIR", r"C:\Users\wn00246424\OneDrive - WGS 365\SHINO")

def default_logger(msg):
    print(msg)

async def pause_if_needed(pause_check, log_func):
    while pause_check():
        log_func("⏸ Paused...")
        await asyncio.sleep(1)

async def run(log_func=default_logger, should_stop_callback=lambda: False, should_pause_callback=lambda: False):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        page = next((p for p in context.pages if "billing.ups.com/ups/billing/invoice" in p.url), None) #Give the default page mentioned in GUI Launcher
        if not page:
            log_func("Invoice page not found.")
            return

        try:
            # === Example 1: Download a blob PDF ===
            if should_stop_callback():
                log_func("⏹ Stopped before blob download.")
                return
            await pause_if_needed(should_pause_callback, log_func)

            pdf_click_xpath = '//*[@id="invoice-table_wrapper"]/div[2]/div/table/tbody/tr[1]/td[10]/div'
            async with context.expect_page() as new_tab_info:
                await page.locator(f"xpath={pdf_click_xpath}").click()
            blob_tab = await new_tab_info.value

            invoice_number = "example_invoice"
            save_path = os.path.join(SAVE_DIR, f"{invoice_number}.pdf")
            await download_blob_pdf_from_tab(blob_tab, save_path)
            await blob_tab.close()
            log_func(f"✅ Blob PDF downloaded: {save_path}")

            if should_stop_callback():
                log_func("⏹ Stopped before alt-click.")
                return
            await pause_if_needed(should_pause_callback, log_func)

            # === Example 2: Alt-click PDF download ===
            alt_click_xpath = '//*[@id="download-link-alt"]'  # Replace with real XPath
            await download_file(
                page=page,
                download_xpath=alt_click_xpath,
                download_folder=SAVE_DIR,
                custom_filename="alt_click_invoice"
            )
            log_func("✅ Alt-click PDF download complete.")

        except Exception as e:
            log_func(f"❌ Error during run: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run())
