from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home', 
            'jpg_to_png',
            'webp_to_jpg',
            'image_to_pdf',
            'image_compress',
            'pdf_to_image',
            'image_to_text',
            'pdf_to_docx',
            'ppt_to_pdf',
            'about',
            'services',
            'search_results'
        ]

    def location(self, item):
        return reverse(item)
