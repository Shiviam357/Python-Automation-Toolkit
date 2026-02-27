import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pillow_heif import register_heif_opener # Modern HEIC support
from datetime import datetime
import threading

# Register HEIF opener with Pillow
register_heif_opener()

class ImageToPDFConverterV2:
    def __init__(self, root):
        self.root = root
        self.root.title("High-Fidelity Converter V2 (WebP & HEIC Support)")
        self.root.geometry("500x300")
        
        # Define supported extensions
        self.supported_formats = [
            ("All Supported Images", "*.jpg *.jpeg *.png *.bmp *.webp *.heic"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("PNG", "*.png"),
            ("WebP", "*.webp"),
            ("HEIC", "*.heic"),
            ("BMP", "*.bmp")
        ]
        
        self.label = tk.Label(root, text="Select images to convert to PDF", font=("Arial", 12))
        self.label.pack(pady=20)
        
        self.btn_select = tk.Button(root, text="Select & Convert Images", command=self.start_conversion, bg="#4CAF50", fg="white", padx=20, pady=10)
        self.btn_select.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Ready", fg="blue")
        self.status_label.pack(pady=10)

    def start_conversion(self):
        files = filedialog.askopenfilenames(title="Select Images", filetypes=self.supported_formats)
        if not files:
            return
        
        # Run conversion in a separate thread to keep UI responsive
        threading.Thread(target=self.process_images, args=(files,), daemon=True).start()

    def process_images(self, files):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = f"Converted_PDFs_{timestamp}"
            os.makedirs(output_folder, exist_ok=True)
            
            log_file = os.path.join(output_folder, "conversion_log.txt")
            
            with open(log_file, "w") as log:
                log.write(f"Conversion Session: {timestamp}\n" + "="*30 + "\n")
                
                for file_path in files:
                    file_name = os.path.basename(file_path)
                    name_wo_ext = os.path.splitext(file_name)[0]
                    
                    self.status_label.config(text=f"Processing: {file_name}...")
                    
                    # Open and convert
                    img = Image.open(file_path)
                    img_rgb = img.convert("RGB")
                    
                    pdf_path = os.path.join(output_folder, f"{name_wo_ext}.pdf")
                    # Save with high quality (300 DPI)
                    img_rgb.save(pdf_path, "PDF", resolution=300.0)
                    
                    log.write(f"SUCCESS: {file_name} -> {name_wo_ext}.pdf\n")

            self.status_label.config(text="Status: All Conversions Complete!", fg="green")
            messagebox.showinfo("Success", f"Converted {len(files)} files!\nSaved in: {output_folder}")
            
        except Exception as e:
            self.status_label.config(text="Status: Error Occurred", fg="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverterV2(root)
    root.mainloop()