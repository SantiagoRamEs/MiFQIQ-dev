from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from .forms import GradeForm
from .models import Professor, Grade, User
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


# Create your views here.
@login_required
def my_grades(request):
    grades = Grade.objects.filter(user=request.user).order_by('-created')
    
    return render(request,'my_grades.html',{
        'grades': grades,
    })

@login_required
def delete_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id, user=request.user)

    if request.method == "POST":
        grade.delete()

    return redirect('my_grades')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('/')

@login_required
def view_professors(request):
    

    professors_qs = Professor.objects.order_by('?')

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

    professors = []

    for prof in professors_qs:
        agg = Grade.objects.filter(professor=prof).aggregate(
            **{f'avg_{f}': Avg(f) for f in rating_fields}
        )

        values = [v for v in agg.values() if v is not None]
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
@login_required
def create_grade(request):
    prof_id = request.GET.get('professor') or request.POST.get('professor')
    professor = get_object_or_404(Professor, id=prof_id) if prof_id else None
    if request.method == 'GET':
        form = GradeForm(initial={'professor': professor.id} if professor else None)
        if professor:
            form.fields['professor'].widget = forms.HiddenInput()
        return render(request, 'create_grade.html',{
            'form': form,
            'professor': professor
        })
    else:
        try:
            form = GradeForm(request.POST)
            if professor:
                form.fields['professor'].widget = forms.HiddenInput()
            new_grade = form.save(commit=False)
            new_grade.user = request.user
            new_grade.save()
            return redirect('profile_professor', professor_id=professor.id) #redirecciona al mismo perfil del docente
        except Exception:
            return render(request,'create_grade.html', {
                'form': form,
                'professor': professor,
                'error': 'Please provide valid data'
            })
        


@login_required
def profile_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    grades = Grade.objects.filter(professor=professor).order_by('-created')

    # Filtro de comentarios
    has_comments = grades.filter(comment__isnull=False).exclude(comment__exact='').exists()

    # Verificar si el usuario ya calificó a este profesor
    user_already_graded = False
    if request.user.is_authenticated:
        user_already_graded = Grade.objects.filter(professor=professor, user=request.user).exists()

    # Calcular estadísticas (mantienes tu lógica actual)
    agg = grades.aggregate(
        avg_puntuality=Avg('puntuality'),
        avg_silabo=Avg('silabo'),
        avg_exam_difficulty=Avg('exam_difficulty'),
        avg_empathy=Avg('empathy'),
        avg_class_environment=Avg('class_environment'),
        avg_class_evaluation=Avg('class_evaluation'),
        avg_grading_consistency=Avg('grading_consistency'),
        avg_teaching_material=Avg('teaching_material'),
    )

    def to_number(v):
        return round(v or 0, 1)

    def to_stars(v):
        n = int(round(v or 0))
        return '⭐' * max(0, min(n, 5))

    stats = {}
    for field in ['puntuality', 'silabo', 'exam_difficulty', 'empathy', 'class_environment',
                  'class_evaluation', 'grading_consistency', 'teaching_material']:
        avg_value = agg.get(f'avg_{field}')
        stats[f'avg_{field}'] = to_number(avg_value)
        stats[f'stars_{field}'] = to_stars(avg_value)

    return render(request, 'profile_professor.html', {
        'professor': professor,
        'grades': grades,
        'stats': stats,
        'has_comments': has_comments,
        'user_already_graded': user_already_graded,  # 👈 añadimos esto
    })

@login_required
def editgrade(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    grade = get_object_or_404(Grade, professor=professor, user=request.user)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('profile_professor', professor_id=professor.id)
    else:
        form = GradeForm(instance=grade)
        form.fields['professor'].widget = forms.HiddenInput()

    return render(request, 'edit_grade.html', {
        'form': form,
        'professor': professor
    })

