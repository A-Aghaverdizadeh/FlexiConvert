from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Search Tools"),
                "type": "text",
                "id": "search-input",
            }
        ),
        label="",
    )


class UploadFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "style": "display:none",
                "id": "jpg_to_png",
                "name": "file",
                "accept": "image/jpeg",
                "multiple": True,
            }
        )
    )


class WebpToJpgForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "style": "display:none",
                "id": "webp_to_jpg",
                "name": "file",
                "accept": "image/webp",
                "multiple": True,
            }
        )
    )


class ImageToPdfForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "style": "display:none",
                "id": "image_to_pdf",
                "name": "file",
                "accept": "image/jpeg, image/png",
                "multiple": True,
            }
        ),
        required=True,
    )


class ImageresizeForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "id": "image_compress",
                "style": "display:none",
                "name": "file",
                "accept": "image/jpeg, image/png, image/webp",
                "multiple": True,
            }
        ),
        required=True,
    )


class PDFUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "id": "pdf_to_image",
                "style": "display:none",
                "name": "file",
                "accept": "application/pdf",
                "multiple": True,
            }
        ),
        required=True,
    )


lang_choices = [
    ("eng", _("English")),
    ("fas", _("Persian")),
]


class ImageToTextForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "id": "image_to_text",
                "style": "display:none",
                "name": "file",
                "accept": "image/jpeg, image/png, image/webp",
            }
        ),
        required=True,
    )
    lang = forms.CharField(
        widget=forms.Select(
            choices=lang_choices,
            attrs={"class": "form-control", "id": "exampleFormControlSelect1"},
        )
    )


class PdfToDocxForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "id": "pdf_to_docx",
                "style": "display:none",
                "name": "file",
                "accept": "application/pdf"
            }
        ),
        required=True
    )


class PptToPDFForm(forms.Form):
    pptx = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "id": "ppt_to_pdf",
                "style": "display:none",
                "name": "file",
                "accept": ".ppt, .pptx"
            }
        ),
        required=True
    )

