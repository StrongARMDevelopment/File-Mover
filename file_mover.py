import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import logging
import time

# Logging setup
logging.basicConfig(filename="file_mover.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def get_creation_year(folder_path):
    """Returns the creation year of a folder."""
    try:
        creation_time = os.path.getctime(folder_path)
        creation_year = time.localtime(creation_time).tm_year
        logging.info(f"Creation year for {folder_path}: {creation_year}")
        return creation_year
    except Exception as e:
        logging.error(f"Error getting creation date for {folder_path}: {e}")
        return None

def get_modified_year(folder_path):
    """Returns the last modified year of a folder."""
    try:
        modified_time = os.path.getmtime(folder_path)
        modified_year = time.localtime(modified_time).tm_year
        logging.info(f"Modified year for {folder_path}: {modified_year}")
        return modified_year
    except Exception as e:
        logging.error(f"Error getting modified date for {folder_path}: {e}")
        return None

def move_folders(source, destination, year, limit, use_modified_date, exclude_folders):
    """Moves project folders based on creation or modified year."""
    try:
        folders = [f for f in os.listdir(source) if os.path.isdir(os.path.join(source, f))]
        moved_count = 0
        
        for folder in folders:
            if folder in exclude_folders:
                logging.info(f"Skipping {folder}: excluded by user.")
                continue
            
            folder_path = os.path.join(source, folder)
            folder_year = get_modified_year(folder_path) if use_modified_date else get_creation_year(folder_path)
            if folder_year == year:
                dest_path = os.path.join(destination, folder)
                
                if os.path.exists(dest_path):
                    logging.warning(f"Skipping {folder}: already exists in archive.")
                    continue
                
                shutil.move(folder_path, dest_path)
                logging.info(f"Moved {folder} to {dest_path}")
                moved_count += 1
                
                if limit and moved_count >= limit:
                    break
        messagebox.showinfo("Process Complete", f"Moved {moved_count} folders.")
    except Exception as e:
        logging.error(f"Error moving folders: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_moving():
    """Runs the moving function in a separate thread."""
    source = source_entry.get()
    destination = destination_entry.get()
    year = int(year_var.get()) if year_var.get().isdigit() else None
    limit = int(limit_var.get()) if limit_var.get().isdigit() else None
    use_modified_date = modified_var.get()
    exclude_folders = [folder.strip() for folder in exclude_var.get().split(',')]
    
    if not source or not destination or not year:
        messagebox.showerror("Error", "Please specify source, destination folders, and year.")
        return
    
    confirm = messagebox.askyesno("Confirm", "Proceed with moving folders?")
    if confirm:
        threading.Thread(target=move_folders, args=(source, destination, year, limit, use_modified_date, exclude_folders), daemon=True).start()

def select_source():
    folder = filedialog.askdirectory()
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def select_destination():
    folder = filedialog.askdirectory()
    if folder:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, folder)

# GUI Setup
root = tk.Tk()
root.title("File Mover")
root.geometry("960x540")

tk.Label(root, text="Source Folder:").pack(pady=5)
source_entry = tk.Entry(root, width=50)
source_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_source).pack(pady=5)

tk.Label(root, text="Destination Folder:").pack(pady=5)
destination_entry = tk.Entry(root, width=50)
destination_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_destination).pack(pady=5)

tk.Label(root, text="Year of Folders to Move:").pack(pady=5)
year_var = tk.StringVar()
year_entry = tk.Entry(root, textvariable=year_var)
year_entry.pack(pady=5)

tk.Label(root, text="Move Limit (0 = No Limit):").pack(pady=5)
limit_var = tk.StringVar(value="0")
limit_entry = tk.Entry(root, textvariable=limit_var)
limit_entry.pack(pady=5)

tk.Label(root, text="Folders to Exclude (comma separated):").pack(pady=5)
exclude_var = tk.StringVar()
exclude_entry = tk.Entry(root, textvariable=exclude_var)
exclude_entry.pack(pady=5)

modified_var = tk.BooleanVar()
tk.Checkbutton(root, text="Use Last Modified Date Instead of Creation Date", variable=modified_var).pack(pady=5)

tk.Button(root, text="Start Moving", command=start_moving).pack(pady=10)
root.mainloop()