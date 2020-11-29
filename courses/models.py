from django.conf import settings
from django.db import models
from core.mail import send_mail_template
from django.utils import timezone


# Create your models here.


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name = models.CharField(
        'Nome', max_length=100
    )
    slug = models.SlugField(
        'Atalho'
    )
    description = models.TextField(
        'Descrição', max_length=100, blank=True
    )
    about = models.TextField(
        'Sobre o Curso',
    )
    start_date = models.DateTimeField(
        'Data de Início', null=True, blank=True
    )
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        'Criado em', auto_now_add=True
    )
    uploaded_at = models.DateTimeField(
        'Atualizado', auto_now=True
    )

    objects = CourseManager()

    def get_absolute_slug(self):
        from django.urls import reverse
        return reverse("courses:details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']


class Lesson(models.Model):

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Numero (ordem)', blank=True)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    uploaded_at = models.DateTimeField('Atualizando em', auto_now=True)

    course = models.ForeignKey(
        'Course', verbose_name='Curso',
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(
        upload_to='lessons/materials',
        blank=True,
        null=True
    )
    lesson = models.ForeignKey(
        'Lesson',
        verbose_name='Aula',
        related_name='materials',
        on_delete=models.CASCADE,
    )

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materiais'


class Enrollment(models.Model):
    # STATUS PENDENTE DOS USUÁRIOS DENTRO DE OUTROS STATUS QUE PODERAM SER ADD
    STATUS_CHOICES = (
        (0, "Pentende"),
        (1, "Aprovado"),
        (2, "Cancelado"),

    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='enrollments', verbose_name='Usuário'
    )
    # LINK CAMPO COM CURSO JÁ EXISTENTES
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE,
        verbose_name='Curso', related_name='enrollments'
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=1, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    uploaded_at = models.DateTimeField('Atualizado em', auto_now=True)

    # PARA ATIVAR ALUNO, ISSO É CHAMADO:'FAT MODEL' DEIXA COISA DO MODEL NELE.
    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # INDICE DE INDICIDADE, ONDE SÓ PODE CADASTRA UM ALUNO POR CURSO
        unique_together = (
            ('user', 'course'),
        )


class Announcement(models.Model):
    course = models.ForeignKey(
        "Course", verbose_name='Curso', related_name='announcements',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em Entrada', auto_now_add=True)
    uploaded_at = models.DateTimeField('Atualizando em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        "Announcement",
        verbose_name='Anuncio', related_name='comments',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        on_delete=models.CASCADE,
    )
    comment = models.TextField('Comentários')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    uploaded_at = models.DateTimeField('Atualizando em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-created_at']


def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1
        )
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, dispatch_uid='post_save'
)
