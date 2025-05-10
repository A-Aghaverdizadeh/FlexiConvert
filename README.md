[🇮🇷 فارسی](README-fa.md)

# FlexiConvert | File Conversion Web App

FlexiConvert is a Django-based web application designed for converting various file formats through an intuitive and user-friendly interface. Built as a portfolio project, it demonstrates a clean and modular architecture using Django’s best practices.

## 🚀 Features

- ✅ Convert images to PDF (JPG/PNG/WebP)
- ✅ Compress image files to reduce size
- ✅ OCR functionality (Text extraction from images) — Supports Persian and English
- ✅ Convert PDF files to Word or images
- ✅ Bilingual interface (English & Persian)
- ✅ Drag and drop support for quick uploads
- ✅ SQLite3 database for local storage and user handling

## 🧩 Project Structure

- converter # Core conversion logic and utilities
- service # Backend processing services
- useraccount # User authentication and account handling
- locale # Language translation files (fa, en)
- media # Uploaded media files
- static # Static frontend assets (JS, CSS, fonts)
- app.sock # (If deployed using a socket server)
- db.sqlite3 # Development database (SQLite)
- manage.py # Django management script
- requirements.txt # Python package dependencies


## 🛠️ Installation Guide

### 1. Clone the project and navigate into it

```bash
git clone https://github.com/yourusername/flexiconvert.git
cd flexiconvert
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```
### 4. Install Tesseract OCR (for OCR functionality)
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fas  # Persian language support
```
Note: For Windows, download the installer from Tesseract GitHub.

### 5. Run initial migrations
```bash
python manage.py migrate
```
### 6. Load initial data (optional)
```bash
python manage.py loaddata converter/fixtures/data2.json
```
### 7. Start the development server
```bash
python manage.py runserver
```
Now visit http://127.0.0.1:8000/ to start using FlexiConvert.

## 📦 Tech Stack

- Python 3.x
- Django
- SQLite3
- HTML / CSS / JavaScript
- Pillow, PyMuPDF, pytesseract, pdf2docx, etc.

📄 License

This project is licensed under the MIT License.
