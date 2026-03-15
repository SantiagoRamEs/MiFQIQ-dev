from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from .forms import GradeForm
from .models import Professor, Grade, User, ProfessorCourse
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Count


# Create your views here.
@login_required
def my_grades(request):

    grades = (
        Grade.objects
        .filter(user=request.user)
        .select_related(
            'professor_course__professor',
            'professor_course__course'
        )
        .order_by('-created')
    )

    return render(request, 'my_grades.html', {
        'grades': grades,
    })


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/')

@login_required
def view_professors(request):

    rating_fields = [
        'puntuality',
        'class_environment',
        'empathy',
        'class_evaluation',
        'exam_difficulty',
        'silabo',
        'grading_consistency',
        'teaching_material',
    ]

    professors_qs = Professor.objects.annotate(
        **{f'avg_{f}': Avg(f'courses_taught__grades__{f}') for f in rating_fields}
    ).order_by('?')

    professors = []

    for prof in professors_qs:

        values = [
            getattr(prof, f'avg_{f}')
            for f in rating_fields
            if getattr(prof, f'avg_{f}') is not None
        ]

        general_avg = round(sum(values) / len(values), 1) if values else 0
        stars = '⭐' * max(0, min(int(round(general_avg)), 5))

        professors.append({
            'professor': prof,
            'general_avg': general_avg,
            'stars': stars,
        })

    return render(request, 'professors.html', {
        'professors': professors,
    })

def login_view(request):
    return render(request, 'login.html')

def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

#CREAR UNA CALIFICACIÓN          
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProfessorCourse, Grade


@login_required
def create_grade(request, pc_id):

    professor_course = get_object_or_404(ProfessorCourse, id=pc_id)

    professor = professor_course.professor

    # evitar que el usuario califique el mismo curso dos veces
    already_graded = Grade.objects.filter(
        professor_course=professor_course,
        user=request.user
    ).exists()

    if already_graded:
        return redirect('profile_professor', pk=professor.id)

    if request.method == 'POST':

        Grade.objects.create(
            professor_course=professor_course,
            user=request.user,
            puntuality=request.POST.get('puntuality'),
            class_environment=request.POST.get('class_environment'),
            empathy=request.POST.get('empathy'),
            class_evaluation=request.POST.get('class_evaluation'),
            exam_difficulty=request.POST.get('exam_difficulty'),
            silabo=request.POST.get('silabo'),
            grading_consistency=request.POST.get('grading_consistency'),
            teaching_material=request.POST.get('teaching_material'),
            comment=request.POST.get('comment'),
        )

        return redirect('profile_professor', pk=professor.id)

    return render(request, 'create_grade.html', {
        'professor_course': professor_course,
        'professor': professor
    })    




#PERFIL DE PROFESOR
def profile_professor(request, pk):

    professor = get_object_or_404(Professor, pk=pk)

    rating_fields = [
        'puntuality',
        'class_environment',
        'empathy',
        'class_evaluation',
        'exam_difficulty',
        'silabo',
        'grading_consistency',
        'teaching_material',
    ]

    # PROMEDIO GENERAL
    grades = Grade.objects.filter(professor_course__professor=professor)

    stats = {}
    for field in rating_fields:
        avg = grades.aggregate(avg=Avg(field))['avg']
        stats[f'avg_{field}'] = round(avg, 2) if avg else None

    # CURSOS DEL PROFESOR
    courses = ProfessorCourse.objects.filter(
        professor=professor
    ).select_related('course')

    course_stats = []

    for pc in courses:

        course_grades = Grade.objects.filter(professor_course=pc)

        data = {
            "pc": pc,
            "total_grades": course_grades.count()
        }

        for field in rating_fields:
            avg = course_grades.aggregate(avg=Avg(field))['avg']
            data[f'avg_{field}'] = round(avg, 2) if avg else None

        # si el usuario ya calificó ese curso
        user_graded = False
        if request.user.is_authenticated:
            user_graded = Grade.objects.filter(
                user=request.user,
                professor_course=pc
            ).exists()

        data["user_graded"] = user_graded

        course_stats.append(data)

    # comentarios
    grades_with_comments = grades.exclude(comment="")

    return render(request, "profile_professor.html", {
        "professor": professor,
        "stats": stats,
        "courses": course_stats,
        "grades": grades_with_comments,
        "has_comments": grades_with_comments.exists()
    })

@login_required
def edit_grade(request, grade_id):

    grade = get_object_or_404(
        Grade,
        id=grade_id,
        user=request.user
    )

    professor = grade.professor_course.professor
    course = grade.professor_course.course

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)

        if form.is_valid():
            form.save()
            return redirect('profile_professor', pk=professor.id)

    else:
        form = GradeForm(instance=grade)

    return render(request, 'edit_grade.html', {
        'form': form,
        'professor': professor,
        'course': course
    })

@login_required
def delete_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id, user=request.user)

    if request.method == "POST":
        grade.delete()

    return redirect('my_grades')