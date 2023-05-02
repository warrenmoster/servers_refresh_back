from django.urls import path 
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('get_servers/', views.server_list, name='server_list'),
    path('add_server/', views.add_server, name='add_server'),
    path('get_token/', views.get_csrf_token, name='get_token'),
    path('delete_server/', views.delete_server, name='delete_server'),
]