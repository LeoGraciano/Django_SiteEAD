from .models import Course, Enrollment, Lesson, Material
from .forms import CommentForm, ContactCourse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .decorators import enrollment_required

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
    created, enrollment = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        # enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')


def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template_name = 'undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course
    }
    return render(request, template_name, context)


@ login_required
@enrollment_required
def announcements(request, slug):
    '''course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')'''
    # Isso a cima virou isso aqui, por decorators
    course = request.course
    template = 'announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all(),
    }
    return render(request, template, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    '''course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição esta pendente')
            return redirect('accounts:dashboard')'''
    # Isso a cima virou isso aqui, por decorators
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template_name = 'lessons.html'
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.erro(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template_name = 'lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template_name = 'material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material,
    }
    return render(request, template_name, context)
