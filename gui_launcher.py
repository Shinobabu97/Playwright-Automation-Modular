import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import asyncio
import json
from datetime import datetime
from main import run

DEFAULT_CONFIG_PATH = "config.json"
DEFAULT_EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEFAULT_OUTPUT_DIR = r"C:\Users\wn00246424\OneDrive - WGS 365\SHINO"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("UPS Invoice Downloader")
        self.root.geometry("700x400")

        self.load_config()

        self.edge_path = tk.StringVar(value=self.config.get("edge_path", DEFAULT_EDGE_PATH))
        self.output_path = tk.StringVar(value=self.config.get("output_path", DEFAULT_OUTPUT_DIR))

        tk.Label(root, text="Path to Edge Executable:").pack(pady=5)
        self.edge_entry = tk.Entry(root, textvariable=self.edge_path, width=60)
        self.edge_entry.pack(pady=5)
        tk.Button(root, text="Browse", command=self.browse_edge).pack(pady=5)

        tk.Label(root, text="Output Directory:").pack(pady=5)
        output_frame = tk.Frame(root)
        output_frame.pack(pady=5)
        self.output_entry = tk.Entry(output_frame, textvariable=self.output_path, width=45)
        self.output_entry.pack(side=tk.LEFT)
        tk.Button(output_frame, text="Set Default", command=self.save_config).pack(side=tk.LEFT, padx=5)

        tk.Button(root, text="Open Edge for Login", command=self.open_edge_debug).pack(pady=5)
        tk.Button(root, text="Run Downloader", command=self.start_download).pack(pady=10)

        self.log_text = tk.Text(root, height=10, width=80)
        self.log_text.pack(pady=10)
        self.log_text.insert(tk.END, "Log initialized...\n")

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
        os.environ["UPS_OUTPUT_DIR"] = self.output_path.get()
        os.environ["UPS_LOG_HANDLER"] = "1"
        threading.Thread(target=lambda: asyncio.run(run(log_func=self.log)), daemon=True).start()

    def log(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        if "error" in message.lower() or "fail" in message.lower():
            self.log_text.insert(tk.END, timestamp, "timestamp")
            self.log_text.insert(tk.END, message + "\n", "error")
        else:
            self.log_text.insert(tk.END, timestamp + message + "\n")
        self.log_text.see(tk.END)

        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("timestamp", foreground="gray")

    def load_config(self):
        if os.path.exists(DEFAULT_CONFIG_PATH):
            with open(DEFAULT_CONFIG_PATH, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        self.config["edge_path"] = self.edge_path.get()
        self.config["output_path"] = self.output_path.get()
        with open(DEFAULT_CONFIG_PATH, "w") as f:
            json.dump(self.config, f)
        messagebox.showinfo("Saved", "Default paths have been saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
