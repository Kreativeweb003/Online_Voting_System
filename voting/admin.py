from django.contrib import admin
from .models import Election, CandidateApplication, Vote


admin.site.register(Election)
admin.site.register(CandidateApplication)
admin.site.register(Vote)