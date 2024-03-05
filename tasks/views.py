from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives


def send_email(user,subject,template):
       
        message = render_to_string(template,{
            'user':user,
            
        })
        
        send_email =EmailMultiAlternatives(subject,'',to =[user.email])
        send_email.attach_alternative(message,"text/html")
        send_email.send()

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'priority':
        tasks = tasks.order_by('-priority')
    elif sort_by == 'category':
        tasks = tasks.order_by('category')

    # Filtering
    filter_category = request.GET.get('filter_category')
    if filter_category:
        tasks = tasks.filter(category=filter_category)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# def task_list(request):
#     tasks = Task.objects.filter(user=request.user)

#     # Sorting
#     sort_by = request.GET.get('sort_by')
#     if sort_by == 'due_date':
#         tasks = tasks.order_by('due_date')
#     elif sort_by == 'priority':
#         tasks = tasks.order_by('-priority')
#     elif sort_by == 'category':
#         tasks = tasks.order_by('category__name')

#     # Filtering
#     filter_category = request.GET.get('filter_category')
#     if filter_category:
#         tasks = tasks.filter(category__name=filter_category)

#     categories = Category.objects.all()

#     return render(request, 'tasks/task_list.html', {'tasks': tasks, 'categories': categories})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            send_email(request.user,"Task Created",'tasks/create_task_email.html')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = True
    task.save()
    send_email(request.user,"Task Completed","tasks/task_completion.html")
    return redirect('task_list')
