# High-Fidelity Image to PDF Converter 🖼️➡️📄

A professional-grade Python tool built with `Tkinter` and `Pillow` to convert images (JPG, PNG, BMP) into high-quality PDFs.

## ✨ Key Features
* **Unique Batching:** Automatically creates timestamped folders for every conversion run.
* **Security:** Uses binary "Magic Number" verification to ensure file integrity.
* **High Fidelity:** Saves PDFs at 300 DPI for print-ready quality.
* **Real-time Logging:** Generates a `log_reports.txt` for every session.
* **User Friendly:** Multi-threaded UI remains responsive during conversion.

## 🛠️ Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install Pillow