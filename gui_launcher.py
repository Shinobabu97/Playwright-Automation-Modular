import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import asyncio
from main_downloader import run

DEFAULT_EDGE_PATH = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("UPS Invoice Downloader")
        self.root.geometry("500x200")

        self.edge_path = tk.StringVar(value=DEFAULT_EDGE_PATH)

        tk.Label(root, text="Path to Edge Executable:").pack(pady=5)
        self.edge_entry = tk.Entry(root, textvariable=self.edge_path, width=60)
        self.edge_entry.pack(pady=5)

        tk.Button(root, text="Browse", command=self.browse_edge).pack(pady=5)
        tk.Button(root, text="Open Edge for Login", command=self.open_edge_debug).pack(pady=5)
        tk.Button(root, text="Run Downloader", command=self.start_download).pack(pady=10)

    def browse_edge(self):
        path = filedialog.askopenfilename(title="Select msedge.exe", filetypes=[("Edge Executable", "msedge.exe")])
        if path:
            self.edge_path.set(path)

    def open_edge_debug(self):
        edge_path = self.edge_path.get()
        if not os.path.isfile(edge_path):
            messagebox.showerror("Error", "Invalid Edge path!")
            return
        os.system(f'start "" "{edge_path}" --remote-debugging-port=9222 --start-maximized https://billing.ups.com/ups/billing/invoice') # give default page to open. Change it main as well

    def start_download(self):
        threading.Thread(target=lambda: asyncio.run(run()), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
