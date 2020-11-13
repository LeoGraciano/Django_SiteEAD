from django.db import models
from django.conf import settings

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

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']


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
        Course, on_delete=models.CASCADE,
        verbose_name='Curso', related_name='enrollments'
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    uploaded_at = models.DateTimeField('Atualizado em', auto_now=True)

    # PARA ATIVAR ALUNO, ISSO É CHAMADO:'FAT MODEL' DEIXA COISA DO MODEL NELE.
    def active(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # INDICE DE INDICIDADE, ONDE SÓ PODE CADASTRA UM ALUNO POR CURSO
        unique_together = (
            ('user', 'course'),
        )
