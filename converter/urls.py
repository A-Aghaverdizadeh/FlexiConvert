from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("jpg_to_png", views.jpg_to_png, name="jpg_to_png"),
    path("download_jpg_to_png", views.download_png, name="download_file_jpg_to_png"),
    path("webp_to_jpg", views.webp_to_jpg, name="webp_to_jpg"),
    path("download_webp_to_jpg", views.download_jpg, name="download_file_webp_to_jpg"),
    path("image_to_pdf", views.image_to_pdf, name="image_to_pdf"),
    path("download_image_to_pdf", views.download_pdf, name="download_file_image_to_pdf"),
    path("image_compress", views.image_compress, name="image_compress"),
    path("download_image_compress", views.download_image, name="download_file_image_compress"),
    path("pdf_to_image", views.pdf_to_images, name="pdf_to_image"),
    path("download_pdf_to_image", views.download_pdf_image, name="download_pdf_to_image"),
    path("image_to_text", views.image_to_text, name="image_to_text"),
    path("download_image_to_text", views.download_text, name="download_image_to_text"),
    path("pdf_to_docx", views.pdf_to_docx, name="pdf_to_docx"),
    path("download_pdf_to_docx", views.download_docx, name="download_pdf_to_docx"),
    # path("ppt_to_pdf", views.ppt_to_pdf, name="ppt_to_pdf"),
    # path("download_ppt_to_pdf", views.download_ppt_pdf, name="download_ppt_to_pdf"),
    path("about", views.about, name="about"),
    path('services', views.services, name='services'),
    path('search_results', views.search_results, name='search_results'),
]
    
