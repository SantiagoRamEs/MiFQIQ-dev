from django.urls import path, include
from . import views


urlpatterns =[
    path('', views.login_view, name = 'home'),
    path('accounts/', include('allauth.urls')),

    path('accounts/', include('allauth.urls')),
    path('logout/', views.custom_logout, name='logout'),

    path('professors/', views.view_professors, name = 'professors'),
    path('professors/<int:pk>/', views.profile_professor, name = 'profile_professor'),

    path('grade/create/<int:pc_id>/',views.create_grade,name='creategrade'),
    path('grade/edit/<int:grade_id>/',views.edit_grade,name='editgrade'),
    
    path('mis-calificaciones/', views.my_grades, name = 'my_grades'),
    path('my-grades/delete/<int:grade_id>/', views.delete_grade, name='delete_grade'),
]

