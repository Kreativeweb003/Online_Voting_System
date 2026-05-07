from django import forms
from .models import CandidateApplication, Election


class CandidateApplicationForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ['position', 'manifesto']
        


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date', 'is_active']