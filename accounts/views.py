from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, EditAccountForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)


def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # PARA AUTO LOGIN APOS CADASTRA
            #user = form.save()
            # user = authenticate(username=form.cleaned_data['username'],
            #                    password=form.cleaned_data['password1']
            #                    )
            #login(request, user)
            # return redirect('core:home')
            # FIM AUTO LOGIN APOS CADASTRA
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
            form = EditAccountForm(instance=request.user)
            context['success'] = True
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