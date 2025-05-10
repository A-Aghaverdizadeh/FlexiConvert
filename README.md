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

/converter # Core conversion logic and utilities
/service # Backend processing services
/useraccount # User authentication and account handling
/locale # Language translation files (fa, en)
/media # Uploaded media files
/static # Static frontend assets (JS, CSS, fonts)
/app.sock # (If deployed using a socket server)
/db.sqlite3 # Development database (SQLite)
/manage.py # Django management script
/requirements.txt # Python package dependencies


## 🛠️ Installation Guide

### 1. Clone the project and navigate into it

```bash
git clone https://github.com/yourusername/flexiconvert.git
cd flexiconvert

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt

sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fas  # Persian language support

python manage.py migrate

python manage.py loaddata converter/fixtures/data2.json

python manage.py runserver

```

## Tech Stack

Python 3.x
Django
SQLite3
HTML / CSS / JavaScript
Pillow, PyMuPDF, pytesseract, pdf2docx, etc.

