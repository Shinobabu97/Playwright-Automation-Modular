Website_Automate/
├── gui_launcher.py
├── main.py
├── config.json               # (created at runtime, dont create it or else it will throw error)
├── downloader/
│   ├── __init__.py
│   ├── blob_download.py
│   └── click_download.py

Power Shell code to generate the above file structure:

New-Item -Path "Website_Automate" -ItemType Directory
New-Item -Path "Website_Automate\gui_launcher.py" -ItemType File
New-Item -Path "Website_Automate\main.py" -ItemType File
New-Item -Path "Website_Automate\downloader" -ItemType Directory
New-Item -Path "Website_Automate\downloader\__init__.py" -ItemType File
New-Item -Path "Website_Automate\downloader\blob_download.py" -ItemType File
New-Item -Path "Website_Automate\downloader\click_download.py" -ItemType File


