from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('course/', views.CourseListView.as_view(), name='course_list'),
    path('course/add/', views.CourseCreateView.as_view(), name='course_add'),   
    path('courses/<slug:slug>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'), 
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
]