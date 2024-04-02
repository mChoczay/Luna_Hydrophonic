from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, AddSystemForm, UpdateSystemForm
from .models import HydroponicSystem


def home(request):

    return render(request, "crudapp/index.html")


# - Register user


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"register_form": form}

    return render(request, "crudapp/register.html", context=context)


# - Login user


def login(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {"login_form": form}

    return render(request, "crudapp/login.html", context=context)


# - Dashboard (visible only for logged in usres)


@login_required(login_url="login")
def dashboard(request):

    hydroponic_system = HydroponicSystem.objects.all()

    context = {"hydroponic_systems": hydroponic_system}

    return render(request, "crudapp/dashboard.html", context=context)


# - Create new record (new hydroponic system)


@login_required(login_url="login")
def add_system(request):

    form = AddSystemForm()

    if request.method == "POST":
        form = AddSystemForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("dashboard")

    context = {"add_system_form": form}

    return render(request, "crudapp/create.html", context=context)


# - Update existing system


@login_required(login_url="login")
def update_system(request, pk):

    system = HydroponicSystem.objects.get(id=pk)

    form = UpdateSystemForm(instance=system)

    if request.method == "POST":
        form = UpdateSystemForm(request.POST, instance=system)

        if form.is_valid():
            form.save()

            return redirect("dashboard")

    context = {"update_system_form": form}

    return render(request, "crudapp/update.html", context=context)


# - View details of a system


@login_required(login_url="login")
def view_system(request, pk):

    all_systems = HydroponicSystem.objects.get(id=pk)
    context = {"system": all_systems}

    return render(request, "crudapp/view.html", context=context)


# - Delete existing system


@login_required(login_url="login")
def delete_system(request, pk):

    system = HydroponicSystem.objects.get(id=pk)

    system.delete()

    return redirect("dashboard")


def logout(request):

    auth.logout(request)

    return redirect("")
