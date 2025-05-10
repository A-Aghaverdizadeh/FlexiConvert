[🇬🇧 English](README.md)

# فلکسی‌کانورت | اپلیکیشن تحت وب تبدیل فرمت فایل

**فلکسی‌کانورت** یک اپلیکیشن تحت وب مبتنی بر Django است که امکان تبدیل فرمت‌های مختلف فایل را با رابط کاربری ساده و دو زبانه (فارسی و انگلیسی) فراهم می‌کند. این پروژه به‌عنوان نمونه‌کار طراحی شده و از ساختار ماژولار و تمیز برخوردار است که توسعه و نگهداری آن را آسان می‌سازد.

## 🚀 امکانات

- ✅ تبدیل تصویر به PDF (فرمت‌های JPG، PNG، WebP)
- ✅ فشرده‌سازی تصویر و کاهش حجم فایل
- ✅ استخراج متن از تصویر (OCR) با پشتیبانی از زبان فارسی و انگلیسی
- ✅ تبدیل PDF به Word یا تصویر
- ✅ پشتیبانی از آپلود فایل با کشیدن و رها کردن (Drag & Drop)
- ✅ پشتیبانی از رابط کاربری چندزبانه
- ✅ طراحی واکنش‌گرا و کاربرپسند

## 🧩 ساختار پروژه
- منطق اصلی تبدیل فایل ها : converter
- service # سرویس‌های پردازش بک‌اند
- useraccount # مدیریت حساب کاربری و ورود/ثبت‌نام
- locale # فایل‌های ترجمه برای زبان‌ها (fa, en)
- media # فایل‌های آپلود شده توسط کاربر
- static # فایل‌های استاتیک شامل CSS، JS و فونت‌ها
- db.sqlite3 # پایگاه داده SQLite برای توسعه
- manage.py # اسکریپت مدیریتی جنگو
- requirements.txt # لیست وابستگی‌های پایتون

## 🛠️ راهنمای نصب و اجرا

### ۱. کلون کردن پروژه و ورود به آن

```bash
git clone https://github.com/yourusername/flexiconvert.git
cd flexiconvert
```
### ۲. ساخت و فعال‌سازی محیط مجازی (Virtual Environment) 
```bash
python -m venv venv
source venv/bin/activate      # در لینوکس یا مک
venv\Scripts\activate         # در ویندوز
```
### ۳. نصب وابستگی‌های پروژه
```bash
pip install -r requirements.txt
```
### ۴. نصب Tesseract برای OCR
در لینوکس (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fas  # پشتیبانی از زبان فارسی
```
توجه: در ویندوز می‌توانید Tesseract را از صفحه گیت‌هاب پروژه دانلود و نصب کنید.

### ۵. اعمال مهاجرت‌ها (Migrations)

```bash
python manage.py migrate
```
### ۶. بارگذاری داده‌های اولیه
```bash
python manage.py loaddata converter/fixtures/data2.json
```
### ۷. اجرای سرور توسعه
```bash
python manage.py runserver
```
اکنون می‌توانید با رفتن به آدرس http://127.0.0.1:8000/ از برنامه استفاده کنید.

## 📦 تکنولوژی‌های استفاده شده

- زبان برنامه نویسی Python 3.x برای بک اند
- فریموورک Django
- دیتابیس SQLite3
- زبان های HTML / CSS / JavaScript برای فرانت
- کتابخانه‌های Pillow، PyMuPDF، pytesseract، pdf2docx و ...

