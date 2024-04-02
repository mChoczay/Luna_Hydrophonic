from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, AddSystemForm, UpdateSystemForm
from .models import HydroponicSystem
import psycopg2

def db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="mydatabase",
        user="postgres",
        password="test1234TEST!@#$"
    )

    return conn

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

    user_id = request.user.id
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM crudapp_hydroponicsystem WHERE user_id = {user_id}')
    rows = cur.fetchall()
    context = {"data": rows}
    cur.close()
    conn.close()

    return render(request, "crudapp/dashboard.html", context=context)


# - Create new record (new hydroponic system)


@login_required(login_url="login")
def add_system(request):
    user_id = int(request.user.id)
    conn = db_connection()
    cur = conn.cursor()

    form = AddSystemForm()
    if request.method == "POST":
        form = AddSystemForm(request.POST)

        if form.is_valid():
            form.save()

            query = f"""
            UPDATE crudapp_hydroponicsystem
            SET user_id = {user_id}
            WHERE id = ( SELECT id FROM crudapp_hydroponicsystem ORDER BY created_at DESC LIMIT 1)
            """
            cur.execute(query)
            conn.commit()

            query = f"""
            INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
            VALUES ({user_id}, ( SELECT id FROM crudapp_hydroponicsystem ORDER BY created_at DESC LIMIT 1), {form.cleaned_data['ph']}, {form.cleaned_data['water_temperature']}, {form.cleaned_data['TDS']})
            """
            cur.execute(query)
            conn.commit()
            
            cur.close()
            conn.close()
            return redirect("dashboard")

    context = {"add_system_form": form}

    return render(request, "crudapp/create.html", context=context)


# - Update existing system


@login_required(login_url="login")
def update_system(request, pk):

    system = HydroponicSystem.objects.get(id=pk)
    form = UpdateSystemForm(instance=system)

    print(pk)

    user_id = int(request.user.id)
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        form = UpdateSystemForm(request.POST, instance=system)

        if form.is_valid():
            form.save()

            query = f"""
            INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
            VALUES ({user_id}, {pk}, {system.ph}, {system.water_temperature}, {system.TDS}) 
            """
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
            return redirect("dashboard")

    context = {"update_system_form": form}

    return render(request, "crudapp/update.html", context=context)


# - View details of a system


@login_required(login_url="login")
def view_system(request, pk):
    user_id = request.user.id
    conn = db_connection()
    cur = conn.cursor()
    query = f"""SELECT created_at, ph, water_temperature, TDS
                FROM sensors 
                WHERE user_id = {user_id} AND system_id = {pk}
                ORDER BY created_at DESC
                LIMIT 10"""
    cur.execute(query)
    rows = cur.fetchall()
    context = {"data": rows}
    cur.close()
    conn.close()

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
