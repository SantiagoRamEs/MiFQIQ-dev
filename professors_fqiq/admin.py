from django.contrib import admin
from .models import Professor, Grade, Course, ProfessorCourse


class GradeAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class ProfessorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Grade, GradeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(ProfessorCourse)