from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_student, name='register'),
    path('students/', views.view_students, name='view_students'),
    path('search/', views.search_student, name='search_student'),
    path('update/', views.update_student, name='update_student'),
    path('delete/', views.delete_student, name='delete_student'),
    path('record-score/', views.record_score, name='record_score'),
    path('export/', views.export_students, name='export_students'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
