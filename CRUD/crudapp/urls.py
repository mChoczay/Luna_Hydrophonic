from django.urls import path
from . import views

urlpatterns = [ 

    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # - CRUD

    path('dashboard', views.dashboard, name="dashboard"),
    path('create', views.add_system, name="create"),
    path('update/<int:pk>', views.update_system, name="update"),
    path('system/<int:pk>', views.view_system, name="view"),
    path('delete/<int:pk>', views.delete_system, name="delete"),

    # - Stream
    path('listener', views.listener, name="listener"),

]