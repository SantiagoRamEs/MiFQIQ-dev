from django.contrib import admin
from .models import Professor, Grade

class GradeAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Grade, GradeAdmin)

is_active = True