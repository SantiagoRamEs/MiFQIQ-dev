from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from .validators import validate_image_size, validate_image_format, validate_image_dimensions
from django.utils.text import slugify
import os

#Tabla de cursos
class Course(models.Model):
    name_course = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_course
    
# Tabla de profesores
class Professor(models.Model):
    #photos-supabase
    def professor_upload_path(instance, filename):
        name, ext = os.path.splitext(filename)
        safe_name = slugify(name)
        return f"professor_photos/{safe_name}{ext}"

    name = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to=professor_upload_path,
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_format, validate_image_dimensions]
        )
    courses = models.ManyToManyField(Course, related_name='professors')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'
        ordering = ['name']

    def __str__(self):
        return self.name



# Tabla de calificaciones
class Grade(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='grades')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='grades')
    #general
    puntuality = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    class_environment = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    empathy = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    class_evaluation = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    exam_difficulty = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    silabo = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    grading_consistency = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    teaching_material = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField(blank = True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_average_rating(self):
        grades = self.grades.all()
        if not grades:
            return 0
        return grades.aggregate(Avg('puntuality'))['puntuality__avg']

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['professor', 'user'], name='unique_professor_user')
        ]

    def __str__(self):
        return f'{self.user.username} → {self.professor.name}'
