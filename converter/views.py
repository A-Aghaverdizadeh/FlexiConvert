import zipfile, PyPDF2, uuid, img2pdf, string, os, base64, logging, io, json, tempfile, pytesseract, ebooklib
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path, convert_from_bytes
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import (
    SearchForm,
    UploadFileForm,
    WebpToJpgForm,
    ImageToPdfForm,
    ImageresizeForm,
    PDFUploadForm,
    ImageToTextForm,
    PdfToDocxForm,
    # PptToPDFForm,
)
from django.contrib import messages
from django.utils.translation import gettext as _
from ebooklib import epub
from tempfile import TemporaryFile
from bs4 import BeautifulSoup
# from fpdf import FPDF
from PIL import Image as PILImage
from PIL import UnidentifiedImageError
from django.conf import settings
from io import BytesIO
from .models import Tool, ToolCategory
from django.db.models import Q
from django.db import DatabaseError
from pdf2docx import Converter, parse
from tempfile import TemporaryDirectory

def home(request):
    context = {}
    return render(request, "converter/home.html", context)

def about(request):
    context = {}
    return render(request, "converter/about.html", context)

def services(request):
    context = {}
    return render(request, "converter/services.html", context)

def search_results(request):
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Tool.objects.translated().filter(
                Q(translations__name__icontains=query)
            ).distinct()

    context = {"results": results, "query": query}
    return render(request, "converter/search_results.html", context)

####

logger = logging.getLogger(__name__)

def jpg_to_png(request):
    if request.method == "POST":
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist("file")
                converted_images = []

                for jpg_image in files:
                    img = PILImage.open(jpg_image)
                    png_image_io = io.BytesIO()
                    img.save(png_image_io, format="PNG")
                    png_image_io.seek(0)

                    converted_images.append((jpg_image.name, png_image_io.getvalue()))

                # Save images in a zip file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for image_name, image_data in converted_images:
                        png_name = image_name.rsplit(".", 1)[0] + ".png"
                        zip_file.writestr(png_name, image_data)

                zip_buffer.seek(0)
                request.session["converted_zip"] = base64.b64encode(
                    zip_buffer.getvalue()
                ).decode("utf-8")
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": form.errors.as_json()})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        form = UploadFileForm()

    converted_zip = request.session.get("converted_zip", None)
    return render(
        request,
        "converter/jpg_to_png.html",
        {"form": form, "converted_zip": converted_zip},
    )

def download_png(request):
    converted_zip_base64 = request.session.get("converted_zip", None)
    if converted_zip_base64:
        converted_zip = base64.b64decode(converted_zip_base64)
        response = HttpResponse(converted_zip, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=converted_images.zip"
        return response
    else:
        messages.error(request, _("No PNG to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
####

def webp_to_jpg(request):
    if request.method == "POST":
        form = WebpToJpgForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("file")
            converted_images = []

            for webp_image in files:
                image = PILImage.open(webp_image)
                with io.BytesIO() as output:
                    image.convert("RGB").save(output, format="JPEG")
                    output.seek(0)
                    converted_images.append((webp_image.name, output.getvalue()))

            # Save images in a zip file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for image_name, image_data in converted_images:
                    jpg_name = image_name.rsplit(".", 1)[0] + ".jpg"
                    zip_file.writestr(jpg_name, image_data)

            zip_buffer.seek(0)
            request.session["converted_zip"] = base64.b64encode(
                zip_buffer.getvalue()
            ).decode("utf-8")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = WebpToJpgForm()

    converted_zip = request.session.get("converted_zip", None)
    return render(
        request,
        "converter/webp_to_jpg.html",
        {"form": form, "converted_zip": converted_zip},
    )

def download_jpg(request):
    converted_zip_base64 = request.session.get("converted_zip", None)
    if converted_zip_base64:
        converted_zip = base64.b64decode(converted_zip_base64)
        response = HttpResponse(converted_zip, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=converted_images.zip"
        return response
    else:
        messages.error(request, _("No Jpg to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

####

def image_to_pdf(request):
    if request.method == "POST":
        form = ImageToPdfForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("file")
            pdf_paths = []

            for img in files:
                img_data = img.read()

                try:
                    img = PILImage.open(BytesIO(img_data))
                except UnidentifiedImageError:
                    continue

                if img.format != "JPEG":
                    buffer = BytesIO()
                    img.convert("RGB").save(buffer, "JPEG")
                    img_data = buffer.getvalue()

                a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
                layout_fun = img2pdf.get_layout_fun(a4inpt)

                with BytesIO() as f:
                    f.write(img2pdf.convert([img_data], layout_fun=layout_fun))
                    f.seek(0)
                    pdf_path = os.path.join(
                        settings.MEDIA_ROOT, "pdfs", f"pdf_{uuid.uuid4()}.pdf"
                    )
                    logger.debug(f"Saving PDF to {pdf_path}")
                    if not os.path.exists(os.path.dirname(pdf_path)):
                        os.makedirs(os.path.dirname(pdf_path))
                    with open(pdf_path, "wb") as pdf_file:
                        pdf_file.write(f.read())
                    pdf_paths.append(pdf_path)

            request.session["pdf_paths"] = pdf_paths
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ImageToPdfForm()

    pdf_paths = request.session.get("pdf_paths", None)
    return render(
        request, "converter/image_to_pdf.html", {"form": form, "pdf_paths": pdf_paths}
    )

def download_pdf(request):
    pdf_paths = request.session.get("pdf_paths", None)
    if pdf_paths:
        merged_pdf_path = os.path.join(settings.MEDIA_ROOT, "merged.pdf")
        pdf_merge = PyPDF2.PdfMerger()

        for pdf_path in pdf_paths:
            with open(pdf_path, "rb") as pdf_file:
                pdf_merge.append(PyPDF2.PdfReader(pdf_file))

        with open(merged_pdf_path, "wb") as merged_pdf_file:
            pdf_merge.write(merged_pdf_file)

        with open(merged_pdf_path, "rb") as merged_pdf_file:
            response = HttpResponse(
                merged_pdf_file.read(), content_type="application/pdf"
            )
            response["Content-Disposition"] = 'attachment; filename="merged.pdf"'
            return response

    else:
        messages.error(request, _("No PDF to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

####

def compress_image(image_file):
    image = PILImage.open(image_file)
    output_io = io.BytesIO()

    image_format = image.format if image.format else "JPEG"

    if image_format.lower() in ["jpg", "jpeg"]:
        image_format = "JPEG"
        image.save(output_io, format=image_format, quality=75, optimize=True)
    elif image_format.lower() == "png":
        image_format = "PNG"
        image = image.convert("P", palette=PILImage.ADAPTIVE)
        image.save(output_io, format=image_format, optimize=True, compress_level=9)
    else:
        image_format = "JPEG"
        image.save(output_io, format=image_format, quality=75, optimize=True)

    output_io.seek(0)
    return InMemoryUploadedFile(
        output_io,
        "ImageField",
        image_file.name,
        image_file.content_type,
        output_io.getbuffer().nbytes,
        None,
    )

def image_compress(request):
    if request.method == "POST":
        form = ImageresizeForm(request.POST, request.FILES)
        if form.is_valid():
            compressed_images = []
            for image_file in request.FILES.getlist("file"):
                compressed_image = compress_image(image_file)
                compressed_images.append(
                    (compressed_image.name, compressed_image.read())
                )

            compressed_zip_io = io.BytesIO()
            with zipfile.ZipFile(compressed_zip_io, "w") as zip_file:
                for name, data in compressed_images:
                    zip_file.writestr(name, data)
            compressed_zip_io.seek(0)

            request.session["compressed_zip"] = compressed_zip_io.read().decode(
                "latin1"
            )

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = ImageresizeForm()

    compressed_zip_available = "compressed_zip" in request.session

    return render(
        request,
        "converter/image_compress.html",
        {"form": form, "compressed_zip_available": compressed_zip_available},
    )

def download_image(request):
    compressed_zip = request.session.get("compressed_zip", None)

    if compressed_zip:
        response = HttpResponse(
            compressed_zip.encode("latin1"), content_type="application/zip"
        )
        response["Content-Disposition"] = "attachment; filename=compressed_images.zip"
        return response
    else:
        messages.error(request, _("No Image to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

####

def pdf_to_images(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["file"]
            output_images = []

            try:
                # Read the PDF file into bytes
                pdf_bytes = pdf_file.read()
                # Convert PDF to images
                images = convert_from_bytes(pdf_bytes, fmt="png")
            except Exception as e:
                logger.error(f"Error converting PDF to images: {e}")
                return JsonResponse({"success": False, "errors": str(e)}, status=500)

            for i, image in enumerate(images):
                img_io = io.BytesIO()
                image.save(img_io, format="PNG")
                img_io.seek(0)
                output_images.append((f"page_{i+1}.png", img_io.read()))

            compressed_zip_io = io.BytesIO()
            with zipfile.ZipFile(compressed_zip_io, "w") as zip_file:
                for name, data in output_images:
                    zip_file.writestr(name, data)
            compressed_zip_io.seek(0)

            request.session["compressed_zip"] = compressed_zip_io.getvalue().decode(
                "latin1"
            )

            return JsonResponse(
                {"success": True, "message": "File compressed and ready for download."}
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = PDFUploadForm()

    return render(request, "converter/pdf_to_image.html", {"form": form})

def download_pdf_image(request):
    compressed_zip = request.session.get("compressed_zip", None)

    if compressed_zip:
        response = HttpResponse(
            compressed_zip.encode("latin1"), content_type="application/zip"
        )
        response["Content-Disposition"] = "attachment; filename=pdf_images.zip"
        return response

    else:
        messages.error(request, _("No Image to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#####

def image_to_text(request):
    if request.method == "POST":
        form = ImageToTextForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["file"]
            lang = form.cleaned_data["lang"]
            img = PILImage.open(image)
            text = pytesseract.image_to_string(img, lang=lang)

            text_io = io.BytesIO()
            text_io.write(text.encode("utf-8"))
            text_io.seek(0)

            request.session["converted_text"] = base64.b64encode(
                text_io.getvalue()
            ).decode("utf-8")
            return JsonResponse({"success": True, "text": text})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = ImageToTextForm()

    return render(
        request,
        "converter/image_to_text.html",
        {"form": form},
    )

def download_text(request):
    converted_text_base64 = request.session.get("converted_text", None)
    if converted_text_base64:
        converted_text = base64.b64decode(converted_text_base64)
        response = HttpResponse(converted_text, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=extracted_text.txt"
        return response
    else:
        messages.error(request, _("No text to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
#####

def pdf_to_docx(request):
    if request.method == "POST":
        form = PdfToDocxForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.cleaned_data["file"]

            try:
                # Create a temporary directory to save the uploaded file
                with TemporaryDirectory() as tmpdirname:
                    tmp_path = os.path.join(tmpdirname, pdf.name)
                    with open(tmp_path, "wb") as tmp_file:
                        tmp_file.write(pdf.read())
                    
                    
                    print(tmpdirname)
                    print(tmp_path)

                    # Convert PDF to DOCX
                    output_path = os.path.join(tmpdirname, "converted.docx")
                    cv = Converter(tmp_path)
                    cv.convert(output_path, start=0, end=None)
                    cv.close()

                    # Read the converted DOCX file and encode it in base64
                    with open(output_path, "rb") as docx_file:
                        docx_data = docx_file.read()
                        request.session["converted_docx"] = base64.b64encode(
                            docx_data
                        ).decode("utf-8")

                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = PdfToDocxForm()

    return render(request, "converter/pdf_to_docx.html", {"form": form})

def download_docx(request):
    converted_docx_base64 = request.session.get("converted_docx", None)
    if converted_docx_base64:
        converted_docx = base64.b64decode(converted_docx_base64)
        response = HttpResponse(
            converted_docx,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = "attachment; filename=converted.docx"
        return response
    else:
        messages.error(request, _("No Docx to download"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#####

# errors

def page404(request, exception):
    return render(request, "errors/404.html", status=404)

def page403(request, exception):
    return render(request, "errors/403.html", status=403)

def page400(request, exception):
    return render(request, "errors/400.html", status=400)

def page500(request):
    return render(request, "errors/500.html", status=500)

# processor

def context_processors(request):
    tools = Tool.objects.all()

    tool_category = ToolCategory.objects.all()

    PUB_Tools = Tool.objects.filter(status=Tool.Status.PUBLISHED)

    category_with_tools = []

    for category in tool_category:
        category_tools = PUB_Tools.filter(category=category)
        category_with_tools.append({
            "category": category,
            "tools": category_tools,
        })

    return {"tools": tools, "search_form": SearchForm(), "category_with_tools": category_with_tools}

