from django.db import models

# Create your models here.


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', max_length=100, blank=True)
    about = models.TextField('Sobre o Curso', )
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
    uploaded_at = models.DateTimeField('Atualizado', auto_now=True)

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
