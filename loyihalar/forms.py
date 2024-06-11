from django.contrib.auth import get_user_model
from django.forms import forms, ModelForm

from hodimlar.models import Department, Blog
from loyihalar.models import Project, status_choices,level_choices,size_choices,speed_choices,type_choices
from .models import Documents, Phase, Task
from django import forms

User = get_user_model()


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['author', 'project_start_date']
        labels = {
            'project_curator': 'Proyekt kuraschisi',
            'project_name': 'Proyekt nomi',
            'project_blog': 'Blog',
            'project_size': 'Hajmi',
            'project_level': 'Darajasi',
            'project_speed': 'Tezligi',
            'project_type': 'Turi',
            'project_department': 'Bo\'lim',
            'project_team': 'Jamoa',
            'project_description': 'Izohi',
            'project_done_percentage': 'Bajarilgan foiz',
            'project_deadline': 'Muddati',
            'project_budget': 'Budjeti',
            'project_status': 'Statusi',
            'project_spent_money': 'Xarajatlar',
            'project_departments': 'Bo\'limlar',
        }
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_size': forms.Select(attrs={'class': 'form-control'},choices=size_choices),
            'project_level': forms.Select(attrs={'class': 'form-control'},choices=level_choices),
            'project_speed': forms.Select(attrs={'class': 'form-control'},choices=speed_choices),
            'project_type': forms.Select(attrs={'class': 'form-control'},choices=type_choices),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project_done_percentage': forms.TextInput(attrs={'class': 'form-control'}),
            'project_deadline': forms.DateInput(attrs={'class': 'form-control'}),
            'project_budget': forms.TextInput(attrs={'class': 'form-control'}),
            'project_status': forms.Select(attrs={'class': 'form-control'},choices=status_choices),
            'project_spent_money': forms.TextInput(attrs={'class': 'form-control'}),
            'project_curator': forms.Select(attrs={'class': 'form-control'}),
            'project_blog': forms.Select(attrs={'class': 'form-control'}),
            'project_team': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'project_departments': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['author', 'project_start_date']
        labels = {
            'project_curator': 'Proyekt kuraschisi',
            'project_name': 'Proyekt nomi',
            'project_blog': 'Blog',
            'project_size': 'Hajmi',
            'project_level': 'Darajasi',
            'project_speed': 'Tezligi',
            'project_type': 'Turi',
            'project_department': 'Bo\'lim',
            'project_team': 'Jamoa',
            'project_description': 'Izohi',
            'project_done_percentage': 'Bajarilgan foiz',
            'project_deadline': 'Muddati',
            'project_budget': 'Budjeti',
            'project_status': 'Statusi',
            'project_spent_money': 'Xarajatlar',
            'project_departments': 'Bo\'limlar',
        }
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_size': forms.Select(attrs={'class': 'form-control'},choices=size_choices),
            'project_level': forms.Select(attrs={'class': 'form-control'},choices=level_choices),
            'project_speed': forms.Select(attrs={'class': 'form-control'},choices=speed_choices),
            'project_type': forms.Select(attrs={'class': 'form-control'},choices=type_choices),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project_done_percentage': forms.TextInput(attrs={'class': 'form-control'}),
            'project_deadline': forms.DateInput(attrs={'class': 'form-control'}),
            'project_budget': forms.TextInput(attrs={'class': 'form-control'}),
            'project_status': forms.Select(attrs={'class': 'form-control'},choices=status_choices),
            'project_spent_money': forms.TextInput(attrs={'class': 'form-control'}),
            'project_curator': forms.Select(attrs={'class': 'form-control'}),
            'project_blog': forms.Select(attrs={'class': 'form-control'}),
            'project_team': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'project_departments': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class AddFileForm(forms.ModelForm):
    url = forms.CharField(max_length=250, label='', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'url-input'}))

    class Meta:
        model = Documents
        fields = ['document']
        exclude = ['url']


class AddPhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = ['phase_name']
        exclude = ['project']


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name']
