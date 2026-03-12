from django.contrib import admin
from .models import Professor, Grade, Course

class GradeAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
    filter_horizontal = ('courses',)

class CourseAdmin(admin.ModelAdmin):
    readonly_field = ("created")

# Register your models here.
admin.site.register(Grade, GradeAdmin)
admin.site.register(Course, CourseAdmin)

is_active = True