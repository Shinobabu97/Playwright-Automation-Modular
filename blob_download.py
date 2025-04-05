import os
import base64

async def download_blob_pdf_from_tab(tab, save_path):
    await tab.wait_for_load_state("networkidle")
    await tab.wait_for_timeout(3000)

    if not tab.url.startswith("blob:"):
        raise ValueError(f"Tab URL is not a blob: {tab.url}")

    blob_data = await tab.evaluate("""
        () => {
            return new Promise((resolve, reject) => {
                try {
                    fetch(window.location.href)
                        .then(resp => {
                            if (!resp.ok) throw new Error('Network response was not ok');
                            return resp.blob();
                        })
                        .then(blob => {
                            const reader = new FileReader();
                            reader.onloadend = () => resolve(reader.result);
                            reader.onerror = () => reject(reader.error);
                            reader.readAsDataURL(blob);
                        })
                        .catch(err => reject(err));
                } catch (e) {
                    reject(e);
                }
            });
        }
    """)

    _, base64_data = blob_data.split(",", 1)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(base64_data))

    print(f"Saved: {save_path}")
