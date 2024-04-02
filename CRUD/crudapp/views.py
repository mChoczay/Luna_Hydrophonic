from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from .forms import CreateUserForm, LoginForm



def home(request):
    return render(request, 'crudapp/index.html')

# - Register user

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login')
    context = {'register_form': form}
    return render(request, 'crudapp/register.html', context=context)


# - Login user

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('')
    context = {'login_form': form}
    return render(request, 'crudapp/login.html', context=context)
