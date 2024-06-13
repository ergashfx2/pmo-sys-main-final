import json
import os.path
import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from zipfile import ZipFile

from config import settings
from .forms import CreateProjectForm, EditProjectForm, AddFileForm, AddPhaseForm, AddTaskForm, PermittedProjectsForm
from .formsets import TaskFormSet
from .models import Project, Phase, Task, Documents, Comments, Problems, PermittedProjects
from django.http import HttpResponse

import shutil

file_extensions = {
    'ai': 'adobe',
    'avi': 'film',
    'bmp': 'file-image',
    'css': 'css3',
    'csv': 'file-csv',
    'doc': 'file-word',
    'docx': 'file-word',
    'eps': 'file-image',
    'exe': 'file-code',
    'flv': 'film',
    'gif': 'file-image',
    'html': 'html5',
    'ico': 'file-image',
    'iso': 'file-archive',
    'jpg': 'file-image',
    'jpeg': 'file-image',
    'js': 'js',
    'mp3': 'file-audio',
    'mp4': 'film',
    'pdf': 'file-pdf',
    'png': 'file-image',
    'ppt': 'powerpoint',
    'pptx': 'powerpoint',
    'psd': 'adobe',
    'rar': 'file-archive',
    'svg': 'file-image',
    'tif': 'file-image',
    'tiff': 'file-image',
    'txt': 'file-alt',
    'wav': 'file-audio',
    'xls': 'file-excel',
    'xlsx': 'file-excel',
    'xml': 'code',
    'zip': 'file-archive'
}


@login_required
def all_projects(request):
    projects = Project.objects.all()
    phases = Phase.objects.all()
    tasks = Task.objects.all()
    return render(request, 'all_projects.html', context={'projects': projects, 'phases': phases, 'tasks': tasks})


@login_required
def myProjects(request):
    projects = Project.objects.filter(author=request.user.pk)
    return render(request, 'my-projects.html', context={'projects': projects})


@login_required
def get_project(request, pk):
    project = Project.objects.filter(pk=pk)
    comments = Comments.objects.filter(project_id=pk)
    problems = Problems.objects.filter(project_id=pk)
    datas = []
    form = AddFileForm
    phases = Phase.objects.filter(project_id=project[0].id)
    for phase in phases:
        datas.append({
            'phase': phase.phase_name,
            'phase_done_percentage': int(phase.phase_done_percentage),
            'tasks': Task.objects.filter(phase=phase.id)
        })
    documents = Documents.objects.filter(project=project[0].id)
    return render(request, 'project_detail.html', context={'project': project, 'datas': datas, 'documents': documents,'comments':comments,'problems':problems})


@login_required
def DetailMyProjects(request, pk):
    form = AddFileForm()
    form2 = AddPhaseForm()
    form3 = TaskFormSet()
    project = Project.objects.filter(pk=pk)
    datas = []
    comments = Comments.objects.filter(project_id=project[0].id)
    problems = Problems.objects.filter(project_id=project[0].id)
    phases = Phase.objects.filter(project_id=project[0].id)
    for phase in phases:
        datas.append({
            'phase': phase.phase_name,
            'phase_id': phase.pk,
            'phase_done_percentage': int(phase.phase_done_percentage),
            'tasks': Task.objects.filter(phase=phase.id),
        })
    if request.method == 'POST':
        form = AddFileForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.cleaned_data.get('document'):
            document = form.save(commit=False)
            doc_type = str(form.cleaned_data.get('document')).split('.')[-1]
            document.type = file_extensions[doc_type]
            document.project = Project.objects.get(pk=pk)
            document.save()
            return redirect('my-projects-detail', pk=pk)
        if form.is_valid() and form.cleaned_data.get('url'):
            document = form.save(commit=False)
            url = str(form.cleaned_data.get('url'))
            document.type = 'link'
            document.url = url
            document.project = Project.objects.get(pk=pk)
            document.save()
            return redirect('my-projects-detail', pk=pk)

        formPhase = AddPhaseForm(request.POST)
        if formPhase.is_valid():
            new_phase = formPhase.save(commit=False)
            new_phase.project = project
            new_phase.save()
            task_formset = TaskFormSet(request.POST, instance=new_phase)
            if task_formset.is_valid():
                task_formset.save()
                redirect('my-projects-detail', pk=pk)
        redirect('my-projects-detail', pk=pk)

    documents = Documents.objects.filter(project=project[0].id).order_by('created_at')
    return render(request, 'my-projects-detail.html',
                  context={'project': project, 'datas': datas,'comments':comments,'problems':problems, 'documents': documents, 'form': form, 'form2': form2,
                           'form3': form3,'project_id':pk})


@login_required
def CreateProject(request):
    form = CreateProjectForm()
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            form.save()
            form.save_m2m()
            return redirect('my-projects')

    return render(request, 'create_project.html', context={'form': form})


class UpdateProject(UpdateView):
    model = Project
    template_name = 'update_project.html'
    form_class = EditProjectForm

    def get_success_url(self):
        return reverse('my-projects')


@login_required
def DeleteProject(request, pk):
    print('working')
    project = Project.objects.filter(pk=pk)
    project.delete()
    return redirect('my-projects')


@login_required
def add_phase(request, pk):
    data = json.loads(request.body)
    phase = Phase.objects.create(phase_name=data['phase_name'], project_id=pk)
    for task in data['tasks']:
        Task.objects.create(project_id=pk, phase_id=phase.id, task_name=task)
    return render(request, template_name='my-projects-detail.html')


@login_required
def update_phase(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        Phase.objects.select_related(pk).filter(pk=pk).update(phase_name=data['phase_name'])
        return redirect('my-projects')
    return redirect('my-projects')


@login_required
def delete_phase(request, pk):
    Phase.objects.select_related(pk).filter(pk=pk).delete()
    return redirect('my-projects')


@login_required
def update_task(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        Task.objects.select_related(pk).filter(pk=pk).update(task_name=data['task_name'])
        return redirect('my-projects')
    return redirect('my-projects')


@login_required
def update_task_percentage(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        Task.objects.select_related(pk).filter(pk=pk).update(task_done_percentage=data['task_done_percentage'])
        phase = Task.objects.filter(pk=pk).values()[0]['phase_id']
        tasks = Task.objects.filter(phase_id=phase)
        phase_done_percentage = 0
        project_done_percentage = 0
        for task in tasks:
            phase_done_percentage += int(task.task_done_percentage)
        final_phase_percentage = phase_done_percentage / len(tasks)
        print(final_phase_percentage)
        phase_obj = Phase.objects.get(pk=phase)
        phase_obj.phase_done_percentage = int(final_phase_percentage)
        phase_obj.save()
        phases = Phase.objects.filter(project_id=phase_obj.project.id)
        for phase in phases:
            project_done_percentage += int(phase.phase_done_percentage)
        final_project_percentage = project_done_percentage / len(phases)
        project_obj = Project.objects.get(pk=phase_obj.project.id)
        print(final_project_percentage)
        project_obj.project_done_percentage = int(final_project_percentage)
        project_obj.save()
        return redirect('my-projects')
    return redirect('my-projects')


@login_required
def delete_task(request, pk):
    Task.objects.select_related(pk).filter(pk=pk).delete()
    return redirect('my-projects')


@login_required
def delete_files(request):
    if request.method == 'POST':
        datas = json.loads(request.body)['datas']
        print(datas)
        for data in datas:
            Documents.objects.filter(id=data).delete()
        return redirect('my-projects')
    return redirect('my-projects')


@login_required
def owned_projects(request):
    projects = Project.objects.filter(project_curator=request.user)
    print(projects)
    return render(request, 'owned_projects.html', context={'projects': projects})


@login_required
def create_archive(request, pk):
    documents = Documents.objects.filter(project_id=pk)
    docs = documents.values_list('document', flat=True)
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    zip_file_path = os.path.join(temp_dir, f'{pk}.zip')
    with ZipFile(zip_file_path, 'w') as zip:
        for doc_path in docs:
            doc_full_path = os.path.join(settings.MEDIA_ROOT, str(doc_path))
            zip.write(doc_full_path, os.path.basename(doc_full_path))

    with open(zip_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{pk}.zip"'
        return response


@login_required
def qualification(request):
    return render(request, 'qualification.html')


@login_required
def spending(request):
    return render(request, 'spendings.html')


@login_required
def post_comment(request,pk):
    if request.method == 'POST':
        comment = json.loads(request.body)['comment']
        Comments.objects.create(project_id=pk,author=request.user ,comment=comment)
        return redirect('my-projects-detail')
    return redirect('my-projects-detail')

@login_required
def edit_comment(request,pk):
    if request.method == 'POST':
        comment = json.loads(request.body)['comment']
        Comments.objects.filter(pk=pk).update(comment=comment)
        pk = Comments.objects.get(pk=pk).project.pk
        return redirect('my-projects-detail',pk)
    return redirect('my-projects-detail',pk)


@login_required
def delete_comment(request,pk):
    Comments.objects.filter(pk=pk).delete()
    pk = Comments.objects.get(pk=pk).project.pk
    return redirect('my-projects-detail',pk)



@login_required
def post_problem(request,pk):
    if request.method == 'POST':
        problem = json.loads(request.body)['problem']
        Problems.objects.create(project_id=pk,author=request.user ,problem=problem)
        return redirect('my-projects-detail',pk)
    return redirect('my-projects-detail',pk)

@login_required
def edit_problem(request,pk):
    if request.method == 'POST':
        problem = json.loads(request.body)['problem']
        Problems.objects.filter(pk=pk).update(problem=problem)
        pk = Problems.objects.get(pk=pk).project.pk
        return redirect('my-projects-detail',pk)
    return redirect('my-projects-detail',pk)


@login_required
def delete_problem(request,pk):
    Problems.objects.filter(pk=pk).delete()
    pk = Problems.objects.get(pk=pk).project.pk
    return redirect('my-projects-detail',pk)

@login_required
def add_team_member(request,pk):
    form = PermittedProjectsForm()
    if request.method == 'POST':
        form = PermittedProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project = Project.objects.get(pk=pk)
            form.save()
        return redirect('my-projects-detail',pk)
    return render(request,'add_project_member.html',context={'form':form})


@login_required
def remove_team_member(request,pk):
    form = PermittedProjectsForm()
    if request.method == 'POST':
        form = PermittedProjectsForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            PermittedProjects.objects.filter(project=pk,user=user).delete()
        return redirect('my-projects-detail',pk)
    return render(request,'remove_project_member.html',context={'form':form})