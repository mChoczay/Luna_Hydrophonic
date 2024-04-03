from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CreateUserForm, LoginForm, AddSystemForm, UpdateSystemForm
from .models import HydroponicSystem
import psycopg2



# - Database connection

def db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="postgres",
            password="test1234TEST!@#$"
        )

    except psycopg2.Error as e:
        print("Database connection error:", e)
        return None

    return conn

# - Stream

def listener(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        system_id = request.POST.get('system_id')
        ph = request.POST.get('ph')
        water_temperature = request.POST.get('water_temperature')
        TDS = request.POST.get('TDS')

        if None in (user_id, system_id):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        conn = db_connection()
        cur = conn.cursor()

        if not ph:
            query = f"""
                        INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
                        VALUES ({user_id},{system_id}, (SELECT ph FROM crudapp_hydroponicsystem WHERE user_id = {user_id} AND system_id = {system_id}) , {water_temperature} , {TDS} )
                        """
        elif not water_temperature:
            query = f"""
                        INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
                        VALUES ({user_id},{system_id}, {ph}, (SELECT water_temperature FROM crudapp_hydroponicsystem WHERE user_id = {user_id} AND system_id = {system_id}) , {TDS} )
                        """
        elif not TDS:  
            query = f"""
                        INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
                        VALUES ({user_id},{system_id}, {ph}, {water_temperature}, (SELECT TDS FROM crudapp_hydroponicsystem WHERE user_id = {user_id} AND system_id = {system_id}) )
                        """
        else:  
            query = f"""
                        INSERT INTO sensors (user_id, system_id, ph, water_temperature, TDS)
                        VALUES ({user_id},{system_id}, {ph}, {water_temperature}, {TDS} )
                        """
        try:
            cur.execute(query)
            conn.commit()
            return JsonResponse({'message': 'Data inserted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            cur.close()
            conn.close()
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# - Home page
    

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
