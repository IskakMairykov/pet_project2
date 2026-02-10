from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Task
from datetime import datetime

@login_required(login_url='login')
def task_list_view(request):
    tasks = Task.objects.filter(owner=request.user)
    errors = []

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        deadline_str = request.POST.get('deadline', '').strip()

        if not title:
            errors.append("Title толтуруңуз")
        if len(description) < 10:
            errors.append("Description минимум 10 символ болушу керек")
        if status not in ['todo', 'in_progress', 'done']:
            errors.append("Status туура эмес")

        # Deadline текшерүү
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            if deadline < timezone.now().date():
                errors.append("Deadline өткөн күн болбошу керек")
        except ValueError:
            errors.append("Deadline формат туура эмес")

        # Эгер ката жок болсо task түзүү
        if not errors:
            Task.objects.create(
                title=title,
                description=description,
                status=status,
                deadline=deadline,
                owner=request.user
            )
            messages.success(request, "Task кошулду")
            # POSTтан кийин форма бошобой, кайра ошол pageде көрсөтө беребиз
            return redirect('task_list')

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'errors': errors
    })



@login_required(login_url='login')
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        deadline_str = request.POST.get('deadline', '').strip()

        if not title:
            messages.error(request, "Title толтуруңуз")
        elif len(description) < 10:
            messages.error(request, "Description минимум 10 символ болушу керек")
        elif status not in ['todo', 'in_progress', 'done']:
            messages.error(request, "Status туура эмес")
        else:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                if deadline < timezone.now().date():
                    messages.error(request, "Deadline өткөн күн болбошу керек")
                else:
                    task.title = title
                    task.description = description
                    task.status = status
                    task.deadline = deadline
                    task.save()
                    messages.success(request, "Task жаңыртылды")
                    return redirect('task_list')
            except ValueError:
                messages.error(request, "Deadline формат туура эмес")

    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required(login_url='login')
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    messages.success(request, "Task өчүрүлдү")
    return redirect('task_list')
