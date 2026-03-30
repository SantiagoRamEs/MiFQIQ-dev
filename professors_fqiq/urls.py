from django.urls import path, include
from . import views

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


#API
router = routers.DefaultRouter()
router.register(r"Professor", views.ProfessorViewSet)
router.register(r"User", views.UserViewSet)
router.register(r"ProfessorCourse", views.ProfessorCourseViewSet)
router.register(r"Course", views.CourseViewSet)
router.register(r"Grade", views.GradeViewSet)



urlpatterns =[
    path('', views.login_view, name = 'login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.custom_logout, name='logout'),

    path('professors/', views.view_professors, name = 'professors'),
    path('professors/<int:pk>/', views.profile_professor, name = 'profile_professor'),

    path('grade/create/<int:pc_id>/',views.create_grade,name='creategrade'),
    path('grade/edit/<int:grade_id>/',views.edit_grade,name='editgrade'),
    
    path('mis-calificaciones/', views.my_grades, name = 'my_grades'),
    path('my-grades/delete/<int:grade_id>/', views.delete_grade, name='delete_grade'),


    #API
    path('api/', include(router.urls)),
    #token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    #DOCUMENTATION
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]

