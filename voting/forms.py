from django import forms
from .models import CandidateApplication, Election



class CandidateApplicationForm(forms.ModelForm):

    class Meta:
        model = CandidateApplication

        fields = [
            'position',
            'manifesto'
        ]

        widgets = {
            'position': forms.TextInput(
                attrs={
                    'class': 'candidate-application-input',
                    'placeholder': 'Enter position'
                }
            ),

            'manifesto': forms.Textarea(
                attrs={
                    'class': 'candidate-application-input',
                    'placeholder': 'Write your manifesto',
                    'rows': 8
                }
            )
        }
        


class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'is_active'
        ]

        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }