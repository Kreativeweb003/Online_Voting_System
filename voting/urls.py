from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:election_id>/', views.apply_candidate, name='apply_candidate'),
    path('vote/<int:election_id>/<int:candidate_id>/', views.vote, name='vote'),
    
    # ADMIN CRUD
    path('admin/elections/', views.admin_election_list, name='admin_election_list'),
    path('admin/elections/create/', views.create_election, name='create_election'),
    path('admin/elections/update/<int:pk>/', views.update_election, name='update_election'),
    path('admin/elections/delete/<int:pk>/', views.delete_election, name='delete_election'),
    
    path('admin/candidates/', views.manage_candidates, name='manage_candidates'),
    path('admin/candidates/approve/<int:app_id>/', views.approve_candidate, name='approve_candidate'),
    path('admin/candidates/reject/<int:app_id>/', views.reject_candidate, name='reject_candidate'),
    path('results/<int:election_id>/', views.election_results, name='election_results'),
    
    path('admin/votes/', views.admin_vote_list, name='admin_vote_list'),
    
    path('election/<int:election_id>/candidates/', views.candidate_list, name='candidate_list'),
    path('applications/', views.my_applications, name='my_applications'),
    path('votes/', views.candidate_votes, name='candidate_votes'),
    path("my-votes/", views.my_votes, name="my_votes"),
]