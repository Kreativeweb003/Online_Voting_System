from django.urls import path
from . import views

urlpatterns = [
    path('voter/', views.voter_dashboard, name='voter_dashboard'),
    path('candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]