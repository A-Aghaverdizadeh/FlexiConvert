from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Email"), "type": "email"}
        ),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password"),
                "type": "password",
            }
        ),
        label="",
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "form-control"})

        self.fields["old_password"].label = ""
        self.fields["old_password"].widget.attrs["placeholder"] = _("Old Password")

        self.fields["new_password1"].label = ""
        self.fields["new_password1"].widget.attrs["placeholder"] = _("New Password")

        self.fields["new_password2"].label = ""
        self.fields["new_password2"].widget.attrs["placeholder"] = _(
            "Confirm New Password"
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "form-control"})

        self.fields["email"].label = ""
        self.fields["email"].widget.attrs["placeholder"] = _("Add your Email")


class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "form-control"})

        self.fields["new_password1"].label = ""
        self.fields["new_password1"].widget.attrs["placeholder"] = _("New Password")

        self.fields["new_password2"].label = ""
        self.fields["new_password2"].widget.attrs["placeholder"] = _(
            "Confirm New Password"
        )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": _("Password"),
            }
        ),
        label="",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": _("Repeat Password"),
            }
        ),
        label="",
    )

    class Meta:
        model = User
        fields = ["email", "username"]

        label = {"email": "", "username": ""}

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email",
                    "placeholder": _("Email"),
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                    "placeholder": _("Username"),
                }
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Passwords don't match"))
        return cd["password2"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error("email", ValidationError(_("This Email Already exists")))
        return cleaned_data


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

        labels = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Username")}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("First Name")}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Last Name")}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Email address")}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditUserInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs["class"] += " is-invalid"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("This email already exists."))
        return email


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "delete_image"]

        labels = {"image": "", "delete_image": ""}

        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "custom-file-input",
                    "type": "file",
                    "id": "customFileLang",
                }
            ),
            "delete_image": forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'customCheck1', 'type': 'checkbox'})
        }

