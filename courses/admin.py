from django.contrib import admin

# Register your models here.
from courses.models import (Course, Enrollment, Announcement, Comment)


class CourseAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'start_date', 'uploaded_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])
