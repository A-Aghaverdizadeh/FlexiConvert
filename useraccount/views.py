from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    PasswordResetDoneView,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import (
    LoginForm,
    CustomPasswordChangeForm,
    CustomPasswordResetConfirmForm,
    UserRegistrationForm,
    EditUserInfoForm,
    EditUserProfileForm,
    CustomPasswordResetForm,
)
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import Profile


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, _("Authenticated Successfully"))
                    return redirect("dashboard")
                else:
                    messages.error(request, _("Disabled account"))
            else:
                messages.error(request, _("Invalid login"))
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "account/login.html", context)


def custom_logout(request):
    logout(request)
    messages.success(request, _("You have been logged out successfully"))
    return redirect("login")


@login_required
def dashboard(request):
    context = {"section": "dashboard"}
    return render(request, "account/dashboard.html", context)

@login_required
def security(request):
    return render(request, 'account/security.html')

@login_required
def settings(request):
    return render(request, 'account/settings.html')


class ChangePassword(PasswordChangeView):
    template_name = "account/change_password.html"
    success_url = reverse_lazy("login")
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, _("Your password has been successfully changed"))
        return super().form_valid(form)


class ResetPasswordConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy("login")
    form_class = CustomPasswordResetConfirmForm
    template_name = "account/password_reset_confirm.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Your password has been successfully changed you can login now"),
        )
        return super().form_valid(form)

class ResetPasswordForm(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    form_class = CustomPasswordResetForm

class ResetPasswordDone(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"



def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data["password"])

            new_user.save()
            messages.success(request, _("Your account has been successfully created"))
            return redirect("login")
        else:
            messages.error(request, _("Please correct the errors below"))
    else:
        user_form = UserRegistrationForm()

    context = {"form": user_form}
    return render(request, "account/register.html", context)


@login_required
def edit(request):
    if request.method == "POST":
        user_form = EditUserInfoForm(request.POST, instance=request.user)
        profile_form = EditUserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, _('Your Profile Updated Successfully!'))
            return redirect('dashboard')
        else:
            messages.error(request, _("Correct the errors below"))
    else:
        user_form = EditUserInfoForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "account/edit.html", context)


