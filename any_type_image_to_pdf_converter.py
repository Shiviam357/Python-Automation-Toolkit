import os
import threading
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Image to PDF Converter")
        self.root.geometry("500x450")
        
        # UI Elements
        self.select_btn = tk.Button(root, text="Step 1: Select Images", command=self.select_files)
        self.select_btn.pack(pady=10)
        
        self.file_listbox = tk.Listbox(root, width=60, height=10)
        self.file_listbox.pack(pady=10)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        
        self.convert_btn = tk.Button(root, text="Step 2: Convert to PDF", state="disabled", command=self.start_conversion)
        self.convert_btn.pack(pady=10)
        
        self.selected_files = []
        self.current_output_folder = ""

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for f in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))
            self.convert_btn.config(state="normal")

    def get_safe_path(self, target_path):
        """Prevents overwriting by adding a suffix if the file exists."""
        base, ext = os.path.splitext(target_path)
        counter = 1
        new_path = target_path
        while os.path.exists(new_path):
            new_path = f"{base}_{counter}{ext}"
            counter += 1
        return new_path

    def check_magic_number(self, file_path):
        """Verifies file type via binary header."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header.startswith(b'\xff\xd8\xff'): return "JPEG"
                if header.startswith(b'\x89PNG'): return "PNG"
                if header.startswith(b'BM'): return "BMP"
        except: return None
        return None

    def start_conversion(self):
        # Create a unique timestamped folder for this specific run
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_output_folder = f"Converted_PDFs_{timestamp}"
        os.makedirs(self.current_output_folder, exist_ok=True)
        
        self.convert_btn.config(state="disabled")
        self.select_btn.config(state="disabled")
        
        # Start the background worker
        threading.Thread(target=self.conversion_worker, daemon=True).start()

    def conversion_worker(self):
        log_path = os.path.join(self.current_output_folder, "log_reports.txt")
        success_count = 0
        fail_count = 0
        
        # Open log once for efficiency
        with open(log_path, "a") as log:
            for i, file_path in enumerate(self.selected_files):
                filename = os.path.basename(file_path)
                fmt = self.check_magic_number(file_path)
                
                if not fmt:
                    log.write(f"[FAILED] {filename} - Invalid Magic Number\n")
                    fail_count += 1
                else:
                    try:
                        img = Image.open(file_path)
                        rgb_img = img.convert("RGB")
                        
                        # Set output path
                        pdf_name = os.path.splitext(filename)[0] + ".pdf"
                        target_path = os.path.join(self.current_output_folder, pdf_name)
                        final_path = self.get_safe_path(target_path)
                        
                        # High-fidelity save at 300 DPI
                        rgb_img.save(final_path, "PDF", resolution=300.0)
                        log.write(f"[SUCCESS] {filename} converted to {os.path.basename(final_path)}\n")
                        success_count += 1
                    except Exception as e:
                        log.write(f"[ERROR] {filename}: {str(e)}\n")
                        fail_count += 1
                
                # Update UI Progress
                self.progress['value'] = ((i + 1) / len(self.selected_files)) * 100
                self.root.update_idletasks()

        # Signal main thread to finish
        self.root.after(0, lambda: self.finish_ui(success_count, fail_count))

    def finish_ui(self, s, f):
        messagebox.showinfo("Complete", f"Conversion Finished!\nSucceeded: {s}\nFailed: {f}")
        os.startfile(self.current_output_folder)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()