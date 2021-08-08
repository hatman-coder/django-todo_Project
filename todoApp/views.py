from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from todoApp.forms import TodoForm
from todoApp.models import todoModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

#HOMEPAGE
def home(request):
    return render(request, 'todoApp/homepage.html')

#SIGN UP USER PAGE
def signupuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('createtodo')
        else:
            return render(request, 'todoApp/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['password1'], request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoApp/signupuser.html', {'form':UserCreationForm(), 'error': 'This username is already taken! Please try another one.'})
        else:
            return render(request, 'todoApp/signupuser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})


#LOGIN USER PAGE
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoApp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoApp/loginuser.html', {'form':AuthenticationForm(), 'error': 'No user found'})
        else:
            login(request, user)
            return redirect('currenttodos')

#LOG OUT USER PAGE
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponse('You are not logged in!')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todoApp/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoApp/createtodo.html', {'form':TodoForm(), 'error': 'Bad data passed in ! Try again !'})

@login_required
def currenttodos(request):
    todos = todoModel.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todoApp/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = todoModel.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todoApp/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(todoModel, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todoApp/viewtodo.html', {'todo': todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoApp/viewtodo.html', {'todo': todo, 'form':form, 'error': 'Bad info !'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(todoModel, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(todoModel, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

def jsonview(request):
    todos = todoModel.objects.filter(user=request.user)
    data = {
        'todos': list(todos.values())
    }
    return JsonResponse(data)
