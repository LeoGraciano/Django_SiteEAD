from django.shortcuts import redirect, render, get_object_or_404
from .models import Course, Enrollment
from .forms import ContactCourse
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    template_name = 'index.html'
    courses = Course.objects.all()
    context = {
        'courses': courses
    }

    return render(request, template_name, context)


def details(request, slug):
    template_name = 'detail.html'
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            context['success'] = "Mensagem enviada com Sucesso"
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    if created:
        enrollment.active()
        return redirect('accounts:dashboard')
