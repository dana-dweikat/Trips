from django.urls import path
from . import views 

app_name = 'app1'

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('new-trip', views.new_trip, name='new_trip'),
    path('add', views.add, name='add'),
    path('view_trip/<int:pk>', views.view_trip, name='view_trip'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('details/<int:pk>', views.details, name='details'),
    path('my-trips', views.my_trips, name='my_trips'),
    path('join/<int:pk>', views.join, name='join'),
    path('cancel/<int:pk>', views.cancel, name='cancel')

]

