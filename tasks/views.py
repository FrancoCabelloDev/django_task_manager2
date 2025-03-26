from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Task
from .forms import TaskForm

# ✅ Vista para listar tareas con filtro (solo del usuario autenticado)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # 🔥 Solo tareas del usuario autenticado
    
    # Obtener filtros de la URL
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')

    # Aplicar filtro de estado si no es "all"
    if status_filter != 'all':
        tasks = tasks.filter(status=status_filter)

    # Aplicar filtro de prioridad si no es "all"
    if priority_filter != 'all':
        tasks = tasks.filter(priority=priority_filter)

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }

    return render(request, 'tasks/task_list.html', context)


# ✅ Vista para crear una tarea (asignándola al usuario autenticado)
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # 🔥 Asignar la tarea al usuario autenticado
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})


# ✅ Vista para actualizar una tarea (solo del usuario autenticado)
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # 🔥 Asegurar que sea del usuario autenticado

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form})


# ✅ Vista para eliminar una tarea (solo del usuario autenticado)
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # 🔥 Asegurar que sea del usuario autenticado

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# ✅ Vista basada en clases (CBV) para listar tareas (opcional, si prefieres usar CBVs)
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # 🔥 Solo tareas del usuario autenticado
