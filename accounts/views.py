from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.forms import EditAccountForm, PasswordResetForm, RegistrationForm
from accounts.models import PasswordReset
from courses.models import Enrollment

# Create your views here.


@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    context = {}
    return render(request, template_name, context)


def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


@ login_required
def edit(request):
    template_name = 'edit.html'
    form = EditAccountForm()
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foi alterado com sucesso')
        return redirect('accounts:dashboard')

    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


# USUÁRIO TROCA SENHA PEDINDO A SENHA ANTIGA E SOLICITANDO QUE DIGITE A NOVA.
@ login_required
def edit_password(request):
    template_name = 'edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
        context['form'] = form
    return render(request, template_name, context)


def password_reset(request):
    template_name = 'password_reset.html'
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'password_reset_confirm.html'
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)
