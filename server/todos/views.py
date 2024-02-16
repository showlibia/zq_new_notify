from django.shortcuts import render,redirect
from .models import Todo  
from django.http import HttpResponseRedirect  
from django.utils import timezone

def todo_list(request):  
    todos = Todo.objects.all().order_by('-created_at')  
    context = {'todos': todos}  
    return render(request, 'todos/todo_list.html', context) 

def add_todo(request):  
    if request.method == 'POST':  
        title = request.POST['title']  
        description = request.POST['description']  
        reminder = request.POST.get('reminder')  
        if reminder:  
            reminder = timezone.make_aware(timezone.datetime.strptime(reminder, '%Y-%m-%d %H:%M:%S'))  
        todo = Todo(title=title, description=description, reminder=reminder)  
        todo.save()  
        return redirect('todo_list')  
    return render(request, 'todos/add_todo.html') 

def todo_complete(request, todo_id):  
    todo = Todo.objects.get(pk=todo_id)  
    todo.completed = not todo.completed  # Toggle the completed status  
    todo.save()  
    return redirect('todo_list')  

def delete_todo(request,todo_id):
    Todo.objects.get(pk=todo_id).delete()
    return redirect("todo_list")


# Create your views here.
