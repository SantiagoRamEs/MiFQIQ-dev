from django.urls import path, include
from . import views


urlpatterns =[
    path('', views.login_view, name = 'home'),
    path('accounts/', include('allauth.urls')),

    path('accounts/', include('allauth.urls')),
    path('logout/', views.custom_logout, name='logout'),

    path('professors/', views.view_professors, name = 'professors'),
    path('professors/<int:professor_id>/', views.profile_professor, name = 'profile_professor'),

    path('creategrade/', views.create_grade, name = 'creategrade'),
    path('editgrade/<int:professor_id>/', views.editgrade, name='editgrade'),
    
    path('mis-calificaciones/', views.my_grades, name = 'my_grades'),
    path('my-grades/delete/<int:grade_id>/', views.delete_grade, name='delete_grade'),


    
]

