from django import forms
from .models import DailyActivity, PersonalGoals

class DailyActivityForm(forms.ModelForm):
    class Meta:
        model = DailyActivity
        fields = ['date', 'water_intake', 'sleep_hours','meditation']
        labels = {
            'date': 'Date',
            'water_intake': 'Water Intake',
            'sleep_hours': 'Sleep Hours ',
            'meditation': 'Meditation',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'water_intake': forms.NumberInput(attrs={'placeholder': 'Liters of water', 'min': '0'}),
            'sleep_hours': forms.NumberInput(attrs={'placeholder': 'Hours of sleep', 'min': '0'}),
            'meditation': forms.NumberInput(attrs={'placeholder': 'Minutes of meditation', 'min': '0'}),
        }


class PersonalGoalsForm(forms.ModelForm):
    class Meta:
        model = PersonalGoals
        fields = ['goal_title', 'goal_description', 'target_date','status']
        labels = {
            'goal_title': 'Goal',
            'goal_description': 'Description',
            'target_date': 'Target date ',
            'status': 'Status',
        }
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'goal_title': forms.TextInput(attrs={'class':'form-control'}),
            'goal_description': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }