import os

async def download_file(page, download_xpath, download_folder, custom_filename=None):
    os.makedirs(download_folder, exist_ok=True)

    async with page.expect_download() as download_info:
        await page.locator(download_xpath).click(modifiers=["Alt"])

    download = await download_info.value

    if not custom_filename:
        custom_filename = download.suggested_filename
    else:
        _, ext = os.path.splitext(download.suggested_filename)
        custom_filename = f"{custom_filename}{ext}"

    custom_download_path = os.path.join(download_folder, custom_filename)
    await download.save_as(custom_download_path)
    print(f"Downloaded via Alt-click: {custom_download_path}")
