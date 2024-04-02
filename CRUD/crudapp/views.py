from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm


def home(request):
    return render(request, 'crudapp/index.html')

# Register view

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login')
    context = {'form': form}
    return render(request, 'crudapp/register.html', context=context)

