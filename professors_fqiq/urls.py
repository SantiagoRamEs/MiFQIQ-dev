from django.urls import path, include
from . import views

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

#API
router = routers.DefaultRouter()
router.register(r"Professor", views.ProfessorViewSet)



urlpatterns =[
    path('', views.login_view, name = 'home'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.custom_logout, name='logout'),

    path('professors/', views.view_professors, name = 'professors'),
    path('professors/<int:pk>/', views.profile_professor, name = 'profile_professor'),

    path('grade/create/<int:pc_id>/',views.create_grade,name='creategrade'),
    path('grade/edit/<int:grade_id>/',views.edit_grade,name='editgrade'),
    
    path('mis-calificaciones/', views.my_grades, name = 'my_grades'),
    path('my-grades/delete/<int:grade_id>/', views.delete_grade, name='delete_grade'),


    #API
    path('api/v1/', include(router.urls)),
    
    #DOCUMENTATION
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

