from django import forms
from .models import SoldierProfile, Assessment, TrainingProgram

class SoldierProfileForm(forms.ModelForm):
    class Meta:
        model = SoldierProfile
        fields = ['rank', 'unit', 'service_number', 'date_of_birth', 'enlistment_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enlistment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['physical_fitness_score', 'technical_skills_score', 'training_score', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
class TrainingProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        fields = ['name', 'description', 'date', 'assigned_unit']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Select CSV File", help_text="File format: Username, Physical Score, Technical Score, Training Score, Comments")
