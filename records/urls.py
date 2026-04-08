from django.urls import path
from . import views

urlpatterns = [
    path('soldiers/', views.soldier_list, name='soldier_list'),
    path('soldiers/<int:pk>/', views.soldier_detail, name='soldier_detail'),
    path('soldiers/<int:pk>/assess/', views.add_assessment, name='add_assessment'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('training/new/', views.create_training_program, name='create_training_program'),
    path('assessments/upload/', views.upload_scores, name='upload_scores'),
]
