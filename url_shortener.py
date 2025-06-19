import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random
import string
import webbrowser
from datetime import datetime
import csv

# In-memory storage
url_mapping = {}
clicks_log = {}

# Generate random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Shorten URL
def shorten_url():
    long_url = entry_long_url.get().strip()
    if not long_url.startswith("http"):
        messagebox.showerror("Invalid URL", "Please enter a valid URL (include http/https).")
        return

    custom_code = entry_custom_code.get().strip()
    short_code = custom_code if custom_code else generate_short_code()

    if short_code in url_mapping:
        messagebox.showerror("Error", "Short code already exists. Try another one.")
        return

    url_mapping[short_code] = long_url
    clicks_log[short_code] = []
    entry_short_code.delete(0, tk.END)
    entry_short_code.insert(0, short_code)

# Open short URL
def open_short_url():
    code = entry_short_code.get().strip()
    if code in url_mapping:
        webbrowser.open(url_mapping[code])
        clicks_log[code].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        messagebox.showerror("Not Found", "Short code not found.")

# Show click timestamps
def show_clicks():
    code = entry_short_code.get().strip()
    if code in clicks_log:
        timestamps = clicks_log[code]
        if timestamps:
            messagebox.showinfo("Click Log", f"{len(timestamps)} Click(s):\n" + "\n".join(timestamps))
        else:
            messagebox.showinfo("Click Log", "No clicks yet.")
    else:
        messagebox.showerror("Not Found", "Short code not found.")

# Show all URLs
def show_all_urls():
    if not url_mapping:
        messagebox.showinfo("No URLs", "No URLs have been shortened yet.")
        return

    all_data = ""
    for code, url in url_mapping.items():
        click_count = len(clicks_log[code])
        all_data += f"{code} → {url}  ({click_count} clicks)\n"

    messagebox.showinfo("All Shortened URLs", all_data)

# Export to CSV
def export_csv():
    if not url_mapping:
        messagebox.showinfo("Nothing to export", "No data to export.")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Short Code", "Original URL", "Clicks", "Timestamps"])
        for code, url in url_mapping.items():
            writer.writerow([code, url, len(clicks_log[code]), "; ".join(clicks_log[code])])
    messagebox.showinfo("Exported", f"Data exported to {filepath}")

# GUI
root = tk.Tk()
root.title("URL Shortener with GUI")
root.geometry("500x450")

tk.Label(root, text="Enter Long URL:").pack()
entry_long_url = tk.Entry(root, width=60)
entry_long_url.pack()

tk.Label(root, text="Custom Short Code (optional):").pack()
entry_custom_code = tk.Entry(root, width=30)
entry_custom_code.pack()

tk.Button(root, text="Shorten URL", command=shorten_url).pack(pady=5)

tk.Label(root, text="Short Code:").pack()
entry_short_code = tk.Entry(root, width=30)
entry_short_code.pack()

tk.Button(root, text="Open Short URL", command=open_short_url).pack(pady=5)
tk.Button(root, text="Show Click Timestamps", command=show_clicks).pack(pady=5)
tk.Button(root, text="Show All Shortened URLs", command=show_all_urls).pack(pady=5)
tk.Button(root, text="Export to CSV", command=export_csv).pack(pady=5)

root.mainloop()
