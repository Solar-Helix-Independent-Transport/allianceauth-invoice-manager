from django.urls import path, re_path

from . import views
from .api import api

app_name = 'invoices'

urlpatterns = [
    path('', views.show_invoices, name='list'),
    path('r/', views.react_main, name='r_list'),
    path('admin/', views.show_admin, name='admin'),
    path('admin_create_tasks/', views.admin_create_tasks, name='admin_create_tasks'),
    re_path(r'^api/', api.urls),
]
