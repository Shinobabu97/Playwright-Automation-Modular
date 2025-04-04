import os

async def download_file(page, download_xpath, download_folder, custom_filename=None):
    """ Clicks on a download link using the given XPath and saves the file to a custom location."""
    os.makedirs(download_folder, exist_ok=True)

    # Expect a download when clicking the link
    async with page.expect_download() as download_info:
        await page.locator(download_xpath).click(modifiers=["Alt"])  # Use Alt-click to download

    download = await download_info.value

    # Determine filename
    if not custom_filename:
        custom_filename = download.suggested_filename
    else:
        _, ext = os.path.splitext(download.suggested_filename)
        custom_filename = f"{custom_filename}{ext}"

    # Final path
    custom_download_path = os.path.join(download_folder, custom_filename)
    await download.save_as(custom_download_path)
    print(f"Downloaded via Alt-click: {custom_download_path}")
